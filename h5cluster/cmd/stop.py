# Copyright © <2019-2020> Varga Consulting, Toronto, On      info@vargaconsulting.ca

from logging import info, critical, warning
from ..auth.rights import protect

@protect('cluster:stop')
def subparser(subparsers, completer):
    stop_parser = subparsers.add_parser("stop", help='stops/hibernates running instances ')
    stop_parser.add_argument(
        "--name", dest='cluster', required=True, metavar='NAME', help='name/tag of the cluster that was specified/generated with start'
    ).completer = completer.names_online

@protect('cluster:stop')
def dispatch(**kwargs):
    info('--------------------------------------------------------------------------------')
    info('                          STOPPING H5CLUSTER                                    ')
    info('--------------------------------------------------------------------------------')
