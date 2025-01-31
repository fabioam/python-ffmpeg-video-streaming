"""
examples.clouds.aws_cloud
~~~~~~~~~~~~

Open a file from a Amazon S3 cloud and save dash files to it


:copyright: (c) 2019 by Amin Yazdanpanah.
:website: https://www.aminyazdanpanah.com
:email: contact@aminyazdanpanah.com
:license: MIT, see LICENSE for more details.
"""

import argparse
import sys

import ffmpeg_streaming
from ffmpeg_streaming import AWS


def aws_cloud(bucket_name, key):
    cloud = AWS(aws_access_key_id='YOUR_KEY_ID', aws_secret_access_key='YOUR_KEY_SECRET')
    download_options = {
        'bucket_name': bucket_name,
        'key': key,
    }
    upload_options = {
        'bucket_name': bucket_name,
    }

    from_aws_cloud = (cloud, download_options, None)
    to_aws_cloud = (cloud, upload_options)

    return from_aws_cloud, to_aws_cloud


def transcode_progress(percentage, ffmpeg):
    # You can update a field in your database
    # You can also create a socket connection and show a progress bar to users
    sys.stdout.write("\rTranscoding...(%s%%)[%s%s]" % (percentage, '#' * percentage, '-' * (100 - percentage)))
    sys.stdout.flush()


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-b', '--bucket_name', required=True, help='Bucket name (required).')
    parser.add_argument('-k', '--key', required=True, help='Key name (required)')

    args = parser.parse_args()

    from_aws_cloud, to_aws_cloud = aws_cloud(args.bucket_name, args.key)

    (
        ffmpeg_streaming
            .dash(from_aws_cloud, adaption='"id=0,streams=v id=1,streams=a"')
            .format('libx265')
            .auto_rep()
            .package('/var/www/media/stream.mpd', to_aws_cloud, transcode_progress)
    )


if __name__ == "__main__":
    sys.exit(main())
