# Copyright © <2019-2020> Varga Consulting, Toronto, On      info@vargaconsulting.ca

from logging import info, error
from ..auth.rights import protect


@protect('cluster:resume')
def subparser(subparsers, completer):
    resume_parser = subparsers.add_parser("resume", help='resuming hibernating/stopped cluster instances')
    resume_parser.add_argument(
        "--name", dest='cluster', required=True, metavar='NAME', help='name/tag of the cluster that was specified/generated with start'
    ).completer = completer.names_online
    resume_parser.add_argument(
        "--dry-run",  action='store_true', help="do test run, skips instantiating nodes...")

@protect('cluster:resume')
def dispatch(**kwargs):
    info('--------------------------------------------------------------------------------')
    info('                          RESUMING H5CLUSTER                                    ')
    info('--------------------------------------------------------------------------------')
