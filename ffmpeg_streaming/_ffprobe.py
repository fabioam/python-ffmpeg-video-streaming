"""
ffmpeg_streaming._ffprobe
~~~~~~~~~~~~

Probe the video


:copyright: (c) 2019 by Amin Yazdanpanah.
:website: https://www.aminyazdanpanah.com
:email: contact@aminyazdanpanah.com
:license: MIT, see LICENSE for more details.
"""

import json
import os
import subprocess
from .streams import Streams


class FFProbe:
    def __init__(self, filename, cmd='ffprobe'):
        args = [cmd, '-show_format', '-show_streams', '-of', 'json', filename]
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.out, err = process.communicate()
        if process.returncode != 0:
            raise RuntimeError('ffprobe', self.out, err)

    def streams(self):
        return Streams(json.loads(self.out.decode('utf-8'))['streams'])

    def format(self):
        return json.loads(self.out.decode('utf-8'))['format']

    def all(self):
        return json.loads(self.out.decode('utf-8'))

    def save_as_json(self, path):
        with open(path, 'w') as probe:
            probe.write(self.out.decode('utf-8'))


def ffprobe(filename, cmd='ffprobe'):
    if not os.path.isfile(filename):
        raise RuntimeError('The file is not exist')
    return FFProbe(filename, cmd)


__all__ = [
    'ffprobe',
    'FFProbe'
]
