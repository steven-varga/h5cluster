# Copyright © <2019-2020> Varga Consulting, Toronto, ON info@vargaconsulting.ca

from inflection import camelize, underscore
import boto3
from ..auth.rights import protect


#NOTICE: flags (true/false) don't use 'true_store' instead must be left empty, and let the parser merge values from default_dict or `.aws/config` 
@protect('s3:mkfs')
def subparser(subparsers, completer):
    parser = subparsers.add_parser("mkfs", help='creates and formats volumes: ebs, s3block, pvfs')
    sp = parser.add_subparsers(title='subparser', dest='sub_cmd', help='additional help')

    # AWS S3 volume
    s3_parser = sp.add_parser("s3", help='formats S3 bucket')
    s3_parser.add_argument("--name",  metavar='NAME', help='bucket name, same as section name [volume s3block:xyz] within .aws/config'
        ).completer = completer.bucket_names
    s3_parser.add_argument("--region",  metavar='NAME', help='aws ec2 region name'
        ).completer = completer.region
    s3_parser.add_argument("--file-system", metavar='VALUE', help='name and optional params, example: ext4 -O ^has_journal')
    s3_parser.add_argument("--block-cache-dir", metavar='PATH', help='local write back cache filename')
    s3_parser.add_argument("--block-cache-size", metavar='VALUE', help='maximum write back cache size, example: 8G'
        ).completer = completer.block_size  
    s3_parser.add_argument('--block-hash-prefix',  help='prepend random prefixes to block object names')
    s3_parser.add_argument('--block-cache-threads',  help='')
    s3_parser.add_argument("--block-size", metavar='VALUE', help='block transfer size')
    s3_parser.add_argument("--compress", metavar='VALUE', help='gzip 0-9')
    s3_parser.add_argument(
        "--volume-size", metavar='VALUE', help='maximum volume size, example: 16T'
        ).completer = completer.block_size
    s3_parser.add_argument("--volume-count",  metavar='VALUE', help='number of disk, defaults to 1')
    s3_parser.add_argument("--access-type",  metavar='VALUE', help='maybe: private | public_read | public_read_write  | authenticated_read')
    s3_parser.add_argument("--timeout", metavar='VALUE', help='wait this many seconds to catch up with block device')
 
    # EBS volume
    ebs_parser = sp.add_parser("ebs", help='formats EBS volume')
    ebs_parser.add_argument("--name", required=True, metavar='NAME', help='section name will be created/used within .aws/config'
        ).completer = completer.instance
    ebs_parser.add_argument("--file-system",  metavar='VALUE', help='name and optional params, example: ext4 -O ^has_journal')
    ebs_parser.add_argument("--size", default="10G", metavar='VALUE', help='single volume size, example 100G'
        ).completer = completer.block_size
    ebs_parser.add_argument("--disk-count", default="1", metavar='VALUE', help='number of disk, defaults to 1')
    ebs_parser.add_argument("--multi-attach",  action='store_true', help="allow EBS volume to be attached to multiple hosts, ony with io1|io2")
    ebs_parser.add_argument("--type", metavar='TYPE', help='volume type: gp2|io1|io2|sc1|st1|standard')
    ebs_parser.add_argument("--iops", metavar='NUM', help='applicable with io1|io2 volumes only')
    ebs_parser.add_argument("--instance-type", default='m5d.large', metavar='TYPE', help='used temporary to create the volumes: m5d.large'
        ).completer = completer.instance
    ebs_parser.add_argument("--region", help='aws ec2 region, uses default section of .aws/config when not set'
        ).completer = completer.region
    ebs_parser.add_argument("--availability-zone", help='EBS volumes must be in the same zone as cluster'
        ).completer = completer.zone
    
    # PVFS
    pvfs_parser = sp.add_parser("pvfs", help='formats volumes for parallel FS')
    pvfs_parser.add_argument("--name",  metavar='NAME', help='section name will be created/used within .aws/config'
        ).completer = completer.instance
    pvfs_parser.add_argument("--instance-type", default='m5d.large', metavar='TYPE', help='used temporary to create the volumes: m5d.large'
        ).completer = completer.instance
def ebs(node): pass

def s3(node): pass

def pvfs(node): pass

_dispatch_ = {
    }

@protect('s3:mkfs')
def dispatch(**kwargs):
    print(**kwargs)
