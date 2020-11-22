# Copyright © <2019-2020> Varga Consulting, Toronto, ON info@vargaconsulting.ca
from inflection import camelize, underscore
import boto3
from ..auth.rights import protect


@protect('mount:s3')
def subparser(subparsers, completer):
    parser = subparsers.add_parser("mount", help='mount S3 bucket locally')
    sp = parser.add_subparsers(title='subparser', dest='sub_cmd', help='additional help')
    s3_parser = sp.add_parser("s3", help='mounts S3 bucket locally')
    s3_parser.add_argument("--name", required=True, metavar='NAME', help='example: s3://region.my-bucket/disk-00'
        ).completer = completer.bucket_names
    s3_parser.add_argument("--mount-dir", metavar='PATH', help='absolute path to mount point'
        ).completer = completer.local_path
    s3_parser.add_argument("--chmod", metavar='VALUE', help='example: a+rw')
    s3_parser.add_argument("--chown", metavar='VALUE', help='example: root:h5cluster')
    s3_parser.add_argument("--ipv4", dest='remote_ipv4', metavar='IPv4', help='execute on a remote host, must have root ssh access')
    s3_parser.add_argument("--region", metavar='NAME', help='example: us-east-2')

    s3_parser.add_argument("--block-cache-size", metavar='VALUE', help='local cache size in number of blocks'
        ).completer = completer.cache_size
    s3_parser.add_argument("--block-cache-dir", metavar='VALUE', help='Specify a file in which to store cached data blocks')
    s3_parser.add_argument("--block-cache-write-delay", metavar='VALUE', help='the maximum time a dirty block can remain in the block cache before it must be written out')
    s3_parser.add_argument("--block-cache-threads", metavar='VALUE', help='Set the size of the thread pool associated with the block cache')
    s3_parser.add_argument("--block-cache-max-dirty", metavar='VALUE', help='Specify a limit on the number of dirty blocks in the block cache')
    s3_parser.add_argument("--block-cache-timeout", metavar='VALUE', help='the maximum time a clean entry can remain in the block cache')
    s3_parser.add_argument("--block-cache-num-protected", metavar='VALUE', help='retain the first NUM blocks in the block cache')
    s3_parser.add_argument("--min-write-delay", metavar='VALUE', help='minimum time in milliseconds between the successful completion of a write')
    s3_parser.add_argument("--md5-cache-size", metavar='VALUE', help='size of the MD5 checksum cache in number of blocks')
    s3_parser.add_argument("--md5-cache-time", metavar='VALUE', help='in milliseconds the time after a block has been successfully written')
    s3_parser.add_argument("--read-ahead", metavar='VALUE', help='number of blocks of read ahead')
    s3_parser.add_argument("--read-ahead-trigger", metavar='VALUE', help='number of blocks that must be read consecutively before the read ahead algorithm is triggered')
    s3_parser.add_argument('--read-only', action='store_true', help='mount filesystem as read only')
    s3_parser.add_argument('--rw',  action='store_true', help='mount filesystem as read only')
    s3_parser.add_argument('--directIO', action='store_true', help='disable kernel caching of the backed file')
    s3_parser.add_argument('--block-cache-sync', action='store_true', help='forces synchronous writes in the block cache layer')

    #pvfs_parser = sp.add_parser("pvfs", help='mounts pvfs locally')
    #pvfs_parser.add_argument("--name", required=True, metavar='NAME', help='file server name, see .aws/config')
    #pvfs_parser.add_argument("--mount-dir", metavar='PATH', help='absolute path to mount point'
    #    ).completer = completer.local_path

_dispatch_ = {
}

@protect('mount:s3')
def dispatch(**kwargs):
    pass
    #_dispatch_[(kwargs['sub_cmd'])](**kwargs).mount()


