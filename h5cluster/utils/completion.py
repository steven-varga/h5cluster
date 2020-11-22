# -*- coding: utf-8 -*-
# Copyright © <2019-2020> Varga Consulting, Toronto, ON info@vargaconsulting.ca
import boto3
import os
import psutil


class Ec2Completion(object):

    def __init__(self, config):
        self.config = config

    def instance(self, **kwargs):
        # this one already is a list
        return self.config.instances

    def bid(self, **kwargs):
        try:
            return [self.config.get(kwargs['parsed_args'].name, 'BID')]
        except Exception:
            return ['n/a']

    def region(self, **kwargs):
        return self.config.regions

    def zone(self, **kwargs):
        return [self.config.aws_zone]

    def size(self, **kwargs):
        try:
            return [self.config.get(kwargs['parsed_args'].name, 'SIZE')]
        except Exception:
            return ['n/a']

    def ip(self, **kwargs):
        try:
            return [self.config.get(kwargs['parsed_args'].name, 'IP')]
        except Exception:
            return ['n/a']

    def tcp_ports(self, **kwargs):
        try:
            return [self.config.get(kwargs['parsed_args'].name, 'TCP_PORTS')]
        except Exception:
            return ['n/a']

    def udp_ports(self, **kwargs):
        try:
            return [self.config.get(kwargs['parsed_args'].name, 'UDP_PORTS')]
        except Exception:
            return ['n/a']

    def ami(self, **kwargs):
        client = boto3.client('ec2')
        try:
            return [self.config.get(kwargs['parsed_args'].name, 'AMI')]
        except Exception:
            try:
                return [key['ImageId'] for key in client.describe_images(ExecutableUsers=['self'])['Images']]
            except Exception:
                return ['n/a']

    def ebs_volumes(self, **kwargs):
        client = boto3.client('ec2')
        try:
            return [self.config.get(kwargs['parsed_args'].name, 'EBS_VOLUMES')]
        except Exception:
            try:
                return [key['VolumeId'] for key in client.describe_volumes()['Volumes']]
            except Exception:
                return ['n/a']

    def ip_address(self, **kwargs):
        client = boto3.client('ec2')
        try:
            return [self.config.get(kwargs['parsed_args'].name, 'IP')]
        except Exception:
            try:
                return [key['PublicIp'] for key in client.describe_addresses()['Addresses']]
            except Exception:
                return ['n/a']

    def vpc(self, **kwargs):
        client = boto3.client('ec2')
        try:
            return [vpc['VpcId'] for vpc in client.describe_vpcs()['Vpcs']]
        except Exception:
            return ['n/a']

    def key(self, **kwargs):
        client = boto3.client('ec2')
        try:
            return [self.config.get(kwargs['parsed_args'].name, 'KEY_NAME')]
        except Exception:
            try:
                return [key['KeyName'] for key in client.describe_key_pairs()['KeyPairs']]
            except Exception:
                return ['n/a']

    def names(self, **kwargs):
        return self.config.cluster_names

    def names_online(self, **kwargs):
        """ cluster names are encoded as `placements groups`
        fetching all placement groups is the same as querying existing clusters on AWS EC2"""
        client = boto3.client('ec2')
        try:
            names = [pg['GroupName'] for pg in client.describe_placement_groups()['PlacementGroups']]
            if not names:
                names.append('n/a')
            return names
        except Exception:
            return self.config.cluster_names

    def bucket_names(self, **kwargs):
        s3 = boto3.client('s3')
        try:
            response = s3.list_buckets()
            names = list()
            for bucket in response['Buckets']:
                names.append('s3://' + bucket["Name"])
            return names
        except Exception:
            return ['n/a']

    def mounted_directory(self, **kwargs):
        return [ dev.mountpoint for dev in psutil.disk_partitions() if dev.mountpoint != '/']

    def local_path(self, **kwargs):
        name = kwargs['parsed_args'].name
        return [name]

    def cache_size(self, **kwargs):
        return ['1024','2048','4096','8192']

    def block_size(self, **kwargs):
        return ['512K','1M','2M','4M', '8M']
