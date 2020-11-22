#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
# Copyright © <2019-2020> Varga Consulting, Toronto, ON info@vargaconsulting.ca

from argparse import RawTextHelpFormatter, ArgumentParser
import argcomplete
import textwrap
import os
import sys
from logging import info, critical, exception
from .cmd import register, start, stop, terminate, resume, add, configure, mkfs, mount, umount, status, ssh
from .conf.parser import ClusterConfigParser
from .utils import completion

# add new commands here, as well as to `subcommand` section in `main()`
# prototype of the dispatch function is `func(arguments)`
dispatch_ = {
    'start': start.dispatch, 'stop': stop.dispatch, 'terminate': terminate.dispatch, 'resume': resume.dispatch,
    'add': add.dispatch, 'configure': configure.dispatch,
    'status': status.dispatch,
    'mount': mount.dispatch,
    'umount': umount.dispatch,
    'mkfs': mkfs.dispatch,
    'register': register.dispatch,
    }


def main():
    # read sections from aws ec2 configuration files to build the context
    config = ClusterConfigParser(
            [os.path.expanduser('~/.ec2config'), os.path.expanduser('~/.aws/config')])
    # some completion results require EC2 context, 'config' is to provide sideband information
    completer = completion.Ec2Completion(config)
    parser = ArgumentParser(
        description=textwrap.dedent("""
        cluster builder for AWS EC2 with built in bash completion. For authentication please
        see/update `~/.ec2config` or `~/.aws/config`. An example configuration  is  provided
        with this distribution.
        To create arbitrary complexity cluster, start with a master node, then gradually  add
        compute and io nodes to a given slurm partition, finally call configure.
        """),
        epilog="Copyright © <2019-2020> Varga Consulting, Toronto, ON      info@vargaconsulting.ca",
        formatter_class=RawTextHelpFormatter)
    subparsers = parser.add_subparsers(title='commands', dest='cmd', help='additional help')
    
    
    # sub command sections are listed here, each of them attached to the same completion engine
    start.subparser(subparsers, completer)
    add.subparser(subparsers, completer)
    configure.subparser(subparsers, completer)
    stop.subparser(subparsers, completer)
    terminate.subparser(subparsers, completer)
    resume.subparser(subparsers, completer)
    status.subparser(subparsers, completer)
    # following have two level parsers:
    # cluster cmd subcmd arg [,args...]  
    mount.subparser(subparsers, completer)
    umount.subparser(subparsers, completer)
    mkfs.subparser(subparsers, completer)
    register.subparser(subparsers, register)

    if len(subparsers._name_parser_map.keys()) < 1:
        sys.exit(-2)
    # autocompletion requires the definitions preceeding the activation, do not move this line
    argcomplete.autocomplete(parser)
    # arguments have two components:
    #    - a set specified in command line, possibly overriding sections specified in configuration
    #    - a set within the `.aws/config` configuration file, to construct complex preset configuration
    # referenced nodes, volumes are converted to parameterized objects, returned value is a pair of
    # (str, dict)
    cmd, args = config.update_with_arguments(
                                parser.parse_args())
    try:
        # based on the dispatch table you find on top of this file, don't forget to add new sub commands
        # to both `dispatch` and to `subparser
        args_ = {k: v for k, v in args.items() if v is not None}
        dispatch_[cmd](**args_)
    except Exception as e:
        # in production comment out `raise`, instead let the error handle in effect
        #raise # uncomment this line to debug application, 
        #critical(e)
        sys.exit(-2)