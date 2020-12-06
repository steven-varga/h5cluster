# Copyright © <2019-2020> Varga Consulting, Toronto, On      info@vargaconsulting.ca

from logging import info, critical, warning
import boto3
from ..auth.rights import protect

@protect('cluster:update')
def subparser(subparsers, completer):
    add_parser = subparsers.add_parser("add", help='add nodes to existing cluster')
    add_parser.add_argument(
        "--name", dest='cluster', required=True, metavar='NAME', help='name/tag of the cluster that was provided when starting cluster'
    ).completer = completer.names_online
    add_parser.add_argument(
        "--group", dest='group', required=True, metavar='NAME', help='cluster node group'
    ).completer = completer.names_online
    add_parser.add_argument("--ami", help='EC2 image id').completer = completer.ami
    add_parser.add_argument(
        "--size", type=int, metavar='N', help='number of nodes instantiated ')
    add_parser.add_argument(
        "--instance-type",   metavar='TYPE',  help='cluster instance (default: %(default)s)'
    ).completer = completer.instance
    add_parser.add_argument(
        "--volumes", metavar='NAME [, ...]', help='optional comma separated volumes listed in `.aws/config`'
    ).completer = completer.ebs_volumes
    add_parser.add_argument(
        "--services", metavar='NAME [, ...]', help='optional comma separated services listed in `.aws/config`'
    )
    add_parser.add_argument(
        "--bid-price",  metavar='PRICE', help='maximum bidding price in USD'
    ).completer = completer.bid
    add_parser.add_argument(
        "--behavior", metavar='PROPERTY', help='how spot requests are placed  `terminate | stop | hibernate`'
    )
    add_parser.add_argument('--no-configure', dest='configure', action='store_false',
                            help='skips configuring cluster, use it with heterogeneous nodes')
    add_parser.set_defaults(configure=True)

@protect('cluster:update')
def dispatch(**kwargs):
    print(kwargs)
