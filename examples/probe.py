"""
examples.probe
~~~~~~~~~~~~

Probe the video


:copyright: (c) 2019 by Amin Yazdanpanah.
:website: https://www.aminyazdanpanah.com
:email: contact@aminyazdanpanah.com
:license: MIT, see LICENSE for more details.
"""

import argparse
import datetime
import os

from ffmpeg_streaming import FFProbe


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input', required=True, help='The path to the video file (required).')

    args = parser.parse_args()

    return FFProbe(args.input)


if __name__ == "__main__":
    ffprobe = main()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    ffprobe.save_as_json(os.path.join(current_dir, 'probe.json'))

    all_media = ffprobe.all()

    video_format = ffprobe.format()

    streams = ffprobe.streams().all()
    videos = ffprobe.streams().videos()
    audios = ffprobe.streams().audios()

    first_stream = ffprobe.streams().first_stream()
    first_video = ffprobe.streams().video()
    first_audio = ffprobe.streams().audio()

    print("all:")
    print(all_media)

    print("format:")
    print(video_format)

    print("streams:")
    print(streams)

    print("videos:")
    for video in videos:
        print(video)

    print("audios:")
    for audio in audios:
        print(audio)

    print("first stream:")
    print(first_stream)

    print("first video:")
    print(first_video)

    print("first audio:")
    print(first_audio)

    print("duration: {}".format(str(datetime.timedelta(seconds=float(video_format.get('duration', 0))))))
    # duration: 00:00:10.496

    print("size: {}k".format(round(int(video_format.get('size', 0)) / 1024)))
    # size: 290k

    print("overall bitrate: {}k".format(round(int(video_format.get('bit_rate', 0)) / 1024)))
    # overall bitrate: 221k

    print("dimensions: {}x{}".format(first_video.get('width', "Unknown"), first_video.get('height', "Unknown")))
    # dimensions: 480x270

    print("video bitrate: {}k".format(round(int(first_video.get('bit_rate', 0)) / 1024)))
    # video bitrate: 149k

    print("audio bitrate: {}k".format(round(int(first_audio.get('bit_rate', 0)) / 1024)))
    # audio bitrate: 64k
