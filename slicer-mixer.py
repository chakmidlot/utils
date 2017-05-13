import argparse
import os
import pathlib
from random import shuffle

import math


get_size_command = 'ffprobe -v error -show_entries format=duration ' \
                           '-of default=noprint_wrappers=1:nokey=1 "{input_video}"'

slice_command = 'ffmpeg -i "{input_video}" -ss {start_second} -t {part_size} "{part_video}"'

join_command = 'ffmpeg -f concat -safe 0 -i "{parts_list}" "{result_video}"'


def parse_args():
    parser = argparse.ArgumentParser(description='Split video into pieces and joins in random order.')
    parser.add_argument('-i', '--input_video', required=True, type=pathlib.Path,
                        help='path to input video')
    parser.add_argument('-w', '--workdir', default=pathlib.Path('.'), type=pathlib.Path,
                        help='directory for saving movie parts and result video')
    parser.add_argument('-t', '--part-size', default=60, type=int,
                        help='size of video parts in seconds')
    parser.add_argument('-c', '--clear-temp-folder', action='store_true',
                        help='remove video parts after result video is created')

    return parser.parse_args()


class SlicerMixer:

    def __init__(self, input_video, part_size, workdir, clear_temp_folder):
        self.clear_temp_folder = clear_temp_folder
        self.workdir = workdir
        self.part_size = part_size
        self.input_video = input_video

        self.data_folder = workdir / 'slicer-mixer-parts'

    def shuffle(self):
        self.prepare_data_folder()

        self.slice()
        self.mix()

    def prepare_data_folder(self):
        self.data_folder.mkdir(exist_ok=True, parents=True)

    def slice(self):
        total_count = int(math.ceil(self.input_video_duration / self.part_size))
        id_size = self._get_number_size(total_count)

        for i in range(total_count):
            part_video = self.data_folder / self._get_part_name(i, id_size)

            command = slice_command.format(
                input_video=self.input_video, start_second=i * self.part_size,
                part_size=self.part_size, part_video=part_video)
            os.system(command)

    def mix(self):
        name = f'result.{self.extension}'

        parts = [f"file '{x}'" for x in self.data_folder.iterdir() if x.name.startswith('part')]
        shuffle(parts)

        order_list_file = self.workdir / 'order.txt'
        order_list_file.open('wt').write('\n'.join(parts))

        command = join_command.format(
            parts_list=order_list_file, result_video=self.workdir / name)
        os.system(command)

    def _get_part_name(self, part_id, id_size):
        part_id_str = str(part_id).zfill(id_size)
        return f'part_{part_id_str}.{self.extension}'

    @property
    def extension(self):
        return self.input_video.name.split('.')[-1]

    @property
    def input_video_duration(self):
        command = get_size_command.format(input_video=self.input_video)
        duration_string = os.popen(command).read()
        print(duration_string)

        return float(duration_string)

    def _get_number_size(self, max_number):
        return int(math.log10(max_number)) + 1


if __name__ == '__main__':
    args = parse_args()

    SlicerMixer(args.input_video, args.part_size,
                args.workdir, args.clear_temp_folder)\
        .shuffle()
