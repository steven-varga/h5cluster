# Copyright © <2019-2020> Varga Consulting, Toronto, On info@vargaconsulting.ca

from logging import info, error
import json
from ..auth.rights import protect

@protect('login:cluster')
def subparser(subparsers, completer):
    status_parser = subparsers.add_parser("status", help='retrieves and prints out status information on given cluster')
    status_parser.add_argument(
        "--name", dest='cluster', required=True, metavar='NAME', help='name/tag of the cluster that was specified/generated with start'
    ).completer = completer.names_online

@protect('login:cluster')
def dispatch(**kwargs):
    print('--------------------------------------------------------------------------------')
    print('                                 H5CLUSTER                                      ')
    print('--------------------------------------------------------------------------------')
