# Copyright © <2019-2020> Varga Consulting, Toronto, ON info@vargaconsulting.ca

from logging import info, warning, critical
from ..auth.authorize_device import AuthorizeDevice
from ..auth.rights import protect

@protect('enroll:cluster')
def subparser(subparsers, completer):
    enroll_parser = subparsers.add_parser("register", help='subscribe to H5CLUSTER services')
    enroll_parser.add_argument("--aws-access-key", help='aws access key to instatiate clusters')
    enroll_parser.add_argument("--aws-secret-key", help='aws secret key')

@protect('enroll:cluster')
def dispatch(**kwargs):
    info('--------------------------------------------------------------------------------')
    info('                           ENROLL with H5CLUSTER                                ')
    info('--------------------------------------------------------------------------------')
