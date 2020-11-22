# Copyright © <2019> Varga Consulting, Toronto, On      info@vargaconsulting.ca

from logging import info, warning
from ..auth.rights import protect

@protect('terminate:cluster')
def subparser(subparsers, completer):
    terminate_parser = subparsers.add_parser("terminate", help='terminate running/stopped cluster instances and free ec2 resources')
    terminate_parser.add_argument(
        "--name", dest='cluster', required=True, metavar='NAME', help='name/tag of the cluster that was specified/generated with start'
    ).completer = completer.names_online

@protect('terminate:cluster')
def dispatch(**kwargs):
    info('--------------------------------------------------------------------------------')
    info('                         TERMINATE H5CLUSTER                                    ')
    info('--------------------------------------------------------------------------------')

