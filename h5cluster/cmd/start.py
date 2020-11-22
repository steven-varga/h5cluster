# _____________________________________________________________________________
# NOTICE:   All  information  contained  herein is, and remains the property of
# Varga Consulting and  its suppliers, if  any. The intellectual and  technical
# concepts  contained  herein  are  proprietary  to  Varga Consulting  and  its
# suppliers and may be covered  by  Canadian  and  Foreign Patents, patents  in
# process, and are protected by trade secret or copyright law. Dissemination of
# this  information or reproduction of  this material is strictly forbidden un-
# less prior written permission is obtained from Varga Consulting.
#
# Copyright © <2019-2020> Varga Consulting, Toronto, ON info@vargaconsulting.ca
# _____________________________________________________________________________

from logging import info, warning, critical
import json
from ..auth.rights import protect

@protect('create:cluster')
def subparser(subparsers, completer):
    start_parser = subparsers.add_parser("start", help='create/start cluster with given properties')
    start_parser.add_argument(
        "--region", help='aws ec2 region, uses default section of .aws/config when not set'
    ).completer = completer.region

    start_parser.add_argument(
        "--availability-zone", help='aws ec2 availability zone, must be within `region`'
    ).completer = completer.zone
    start_parser.add_argument("--ami", help='EC2 image id').completer = completer.ami
    start_parser.add_argument(
        "--volumes", metavar='NAME [, ...]', help='optional comma separated volumes listed in `.aws/config`'
    )
    start_parser.add_argument(
        "--services", metavar='NAME [, ...]', help='optional comma separated services listed in `.aws/config`'
    )
    start_parser.add_argument(
        "--nodes", metavar='NODES', help='list of nodes')
    start_parser.add_argument(
        "--instance-type", metavar='TYPE', help='cluster instance type, for instance: m5d.metal'
                                    ).completer = completer.instance
    start_parser.add_argument(
        "--bid-price",  metavar='PRICE', type=float, help='maximum bidding price in USD'
    ).completer = completer.bid
    # https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-requests.html#fixed-duration-spot-instances
    start_parser.add_argument( 
        "--duration",  metavar='TIME', type=int, help='fixed time linght guaranteed price, if specified'
    )
    start_parser.add_argument(
        "--name", dest='cluster', metavar='NAME', help='unique name/tag of the cluster to track state'
    ).completer = completer.names
    start_parser.add_argument(
        "--tcp-ports", metavar='PORT [, ...]', help='list of external IP ports, SSH required').completer = completer.tcp_ports
    start_parser.add_argument(
        "--udp-ports", metavar='PORT [, ...]', help='optional list of UDP ports').completer = completer.udp_ports
    start_parser.add_argument(
        "--ipv4", metavar='ADDRESS', help='elastic IP for master node').completer = completer.ip_address
    start_parser.add_argument(
        "--hostname", metavar='NAME', help='hostname used for ssh connection')
    start_parser.add_argument('--no-configure', dest='configure', action='store_false',
                              help='skips configuring cluster, use it with heterogeneous nodes or for new AMI')
    start_parser.add_argument(
        "--behavior", metavar='PROPERTY', help='how spot requests are placed  `terminate | stop | hibernate`'
    )
    start_parser.set_defaults(configure=True)
    start_parser.add_argument(
        "--dry-run",  action='store_true', help="do test run, skips instantiating nodes...")

# called from `cli.py` with parsed arguments, where nodes, volumes, services are converted to 
# objects, See `parser.py` for details
@protect('create:cluster')
def dispatch(**kwargs):
    info('--------------------------------------------------------------------------------')
    info('                           STARTING H5CLUSTER                                   ')
    info('--------------------------------------------------------------------------------')


