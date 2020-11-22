# Copyright © <2019-2020> Varga Consulting, Toronto, ON info@vargaconsulting.ca
import boto3
from ..auth.rights import protect

@protect('unmount:s3')
def subparser(subparsers, completer):
    unmount_parser = subparsers.add_parser("umount", help='unmount a device that already has been mounted')
    unmount_parser.add_argument(
        "--dir", required=True, metavar='NAME', help='example: /mnt/spack'
    ).completer = completer.mounted_directory
    unmount_parser.add_argument("--ipv4", dest='remote_ipv4', metavar='IPv4', help='execute on a remote host, must have root ssh access')

@protect('unmount:s3')
def dispatch(**kwargs):
    pass
