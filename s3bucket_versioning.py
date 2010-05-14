#!/usr/bin/env python

import os
import sys
import ConfigParser
from optparse import OptionParser
from boto.s3.connection import S3Connection
from boto.exception import BotoClientError

class S3BucketHelper(object):
    def __init__(self, access_key, secret_key):
        self.conn = S3Connection(access_key, secret_key)

    def get_versioning_status(self, bucket):
        ret = bucket.get_versioning_status()
        try:
            return ret["Versioning"]
        except KeyError:
            return "Disabled"

    def is_versioning(self, bucket_name, bucket=None):
        if not bucket:
            bucket = self.conn.get_bucket(bucket_name)
        print "Versioning: %s" % self.get_versioning_status(bucket)

    def enable_versioning(self, bucket_name, enable):
        context = "Disabling"
        if enable: context = "Enabling"
        print "%s versioning for bucket %s" % (context, bucket_name)
        
        bucket = self.conn.get_bucket(bucket_name)

        sys.stdout.write('Before change - ')
        self.is_versioning(bucket_name, bucket)

        bucket.configure_versioning(enable)

        sys.stdout.write('After change - ')
        self.is_versioning(bucket_name, bucket)

    def list_buckets(self):
        for bucket in self.conn.get_all_buckets():
            try:
                print '%s %s' % (bucket.name.ljust(40), self.get_versioning_status(bucket))
            except BotoClientError, e:
                print "Error with bucket: %s" % bucket.name
                print "Error was: %s" % e

def main():
    config_filename = "%s/.s3bucket_versioning.cfg" % os.getenv("HOME")

    parser = OptionParser()
    parser.add_option("-c", "--config", 
        dest="config_filename", 
        default=config_filename, 
        help="Config file name. Defaults to %s" % config_filename
    )
    parser.add_option("-l", "--list",
        dest="list",
        action="store_true",
        default=False,
        help="Lists all buckets and their versioning status.  Beware: This is very slow!"
    )
    parser.add_option("-e", "--enable", 
        dest="enable",
        action="store_true",
        help="Enable versioning on the bucket",
        default=False
    )
    parser.add_option("-d", "--disable", 
        dest="disable", 
        action="store_true",
        help="Disable versioning on the bucket",
        default=False
    )

    (options, args) = parser.parse_args()
    config = ConfigParser.RawConfigParser()
    config.read(options.config_filename)

    bucket_helper = S3BucketHelper(
        config.get('aws_keys', 'access_key'),
        config.get('aws_keys', 'secret_key')
    )

    if options.list:
        #argument free commands
        bucket_helper.list_buckets()
    else:
        # Execute methods requiring the bucket name
        if len(args) != 1:
            parser.error("Please enter a bucket name")

        if options.enable and options.disable:
            parser.error("options -e/--enable and -d/--disable are mutually exclusive")

        bucket_name = args[0]
        if options.enable:
            bucket_helper.enable_versioning(bucket_name, True)
        elif options.disable:
            bucket_helper.enable_versioning(bucket_name, False)
        else:
            bucket_helper.is_versioning(bucket_name)

if __name__ == '__main__':
    main()
