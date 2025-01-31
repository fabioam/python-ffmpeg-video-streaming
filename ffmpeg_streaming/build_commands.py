"""
ffmpeg_streaming.build_commands
~~~~~~~~~~~~

Build a command for the FFmpeg


:copyright: (c) 2019 by Amin Yazdanpanah.
:website: https://www.aminyazdanpanah.com
:email: contact@aminyazdanpanah.com
:license: MIT, see LICENSE for more details.
"""

from .utiles import get_path_info
from .rep import Representation


def _get_hls_args(hls):
    dirname, name = get_path_info(hls.output)

    commands = []
    for rep in hls.reps:
            if isinstance(rep, Representation):
                if hls.options is not None:
                    for option in hls.options:
                        commands += ['-' + option, hls.options[option]]
                commands += ['-s:v', rep.size]
                commands += ['-crf', '20']
                commands += ['-sc_threshold', '0']
                commands += ['-g', '48']
                commands += ['-keyint_min', '48']
                commands += ['-hls_list_size', '0']
                commands += ['-hls_time', str(hls.hls_time)]
                commands += ['-hls_allow_cache', str(hls.hls_allow_cache)]
                commands += ['-b:v', rep.bit_rate]
                if rep.audio_bit_rate is not None:
                    commands += ['-b:a', rep.audio_bit_rate]
                commands += ['-maxrate', str(round(rep.kilo_bitrate * 1.2)) + "k"]
                commands += ['-hls_segment_filename', dirname + "/" + name + "_" + str(rep.height) + "p_%04d.ts"]
                if hls.hls_key_info_file is not None:
                    commands += ['-hls_key_info_file', hls.hls_key_info_file.replace("\\", "/")]
                commands += ['-strict', hls.options.get('strict', "-2")]
                commands += [dirname + "/" + name + "_" + str(rep.height) + "p.m3u8"]

    return commands


def _get_dash_args(dash):
    dirname, name = get_path_info(dash.output)

    commands = [
        '-bf', '1',
        '-keyint_min', '120',
        '-g', '120',
        '-sc_threshold', '0',
        '-b_strategy', '0',
        '-use_timeline', '1',
        '-use_template', '1',
        '-f', 'dash'
    ]

    if dash.options is not None:
        for option in dash.options:
            commands += ['-' + option, dash.options[option]]

    count = 0
    for rep in reversed(dash.reps):
            if isinstance(rep, Representation):
                commands += ['-map', '0']
                commands += ['-b:v:' + str(count), rep.bit_rate]
                if rep.audio_bit_rate is not None:
                    commands += ['-b:a:' + str(count), rep.audio_bit_rate]
                commands += ['-s:v:' + str(count), rep.size]
                count += 1

    if dash.adaption is not None:
        commands += ['-adaptation_sets', dash.adaption]
    commands += ['-strict', dash.options.get('strict', "-2")]
    commands += ['"' + dirname + '/' + name + '.mpd"']

    return commands


def build_command(cmd, media_obj):
    if type(cmd) != list:
        cmd = [cmd]

    cmd += ['-y', '-i', '"' + media_obj.filename.replace("\\", "/") + '"']
    cmd += ['-c:v', media_obj.video_format]

    if media_obj.audio_format is not None:
        cmd += ['-c:a', media_obj.audio_format]

    media_name = type(media_obj).__name__

    if media_name == 'HLS':
        cmd += _get_hls_args(media_obj)
    elif media_name == 'DASH':
        cmd += _get_dash_args(media_obj)

    return " ".join(cmd)
