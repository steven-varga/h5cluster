# Copyright © <2019-2020> Varga Consulting, Toronto, ON info@vargaconsulting.ca

from logging import info, warning, critical, error
from ..auth.rights import protect

@protect('cluster:update')
def subparser(subparsers, completer):
    configure_parser = subparsers.add_parser("configure", help='(re)configures a running cluster')
    configure_parser.add_argument(
        "--name", dest='cluster', required=True, metavar='NAME', help='name of a cluster, same as placement group'
    ).completer = completer.names_online
    configure_parser.add_argument(
        "--dry-run",  action='store_true', help="do test run, skips instantiating nodes...")

@protect('cluster:update')
def dispatch(**kwargs):
    info('--------------------------------------------------------------------------------')
    info('                        CONFIGURING H5CLUSTER                                ')
    info('--------------------------------------------------------------------------------')
