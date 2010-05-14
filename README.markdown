# s3bucket_versioning

A command line tool to manage versioning on Amazon S3 buckets.

### Dependencies

Boto - http://code.google.com/p/boto/

### Installing

You'll need an uptodate version of Boto.  I suggest you install from the SVN trunk using pip:

    sudo pip install svn+http://boto.googlecode.com/svn/trunk/

### Configuration

In your home directory you'll need a config file named .s3bucket_versioning.cfg with the contents being your AWS
access and secret keys.

    [aws_keys]
    access_key: the_access_key
    secret_key: the_secret_key

### Usage

    Usage: s3bucket_versioning.py [options]
    
    Options:
      -h, --help            show this help message and exit
      -c CONFIG_FILENAME, --config=CONFIG_FILENAME
                            Config file name. Defaults to
                            ~/.s3bucket_versioning.cfg
      -l, --list            Lists all buckets and their versioning status.
                            Beware: This is very slow!
      -e, --enable          Enable versioning on the bucket
      -d, --disable         Disable versioning on the bucket

### Future Features

*   View all the versions of a specifc file
