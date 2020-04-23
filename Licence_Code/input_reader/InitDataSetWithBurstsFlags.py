import json
import os
import sys

from input_reader.CreateDOAWithBurstsFlags import CreateDOAWithBurstsFlags

doa_info = {
    'deep': {
        'epd': 'M014_S001_SRCS3L_25,50,100_0002.epd',
        'eti': 'Results M014_S001_SRCS3L_25,50,100_0002 Variable contrast, all orientations.eti'
    },
    'medium': {
        'epd': 'M014_S001_SRCS3L_25,50,100_0003.epd',
        'eti': 'Results M014_S001_SRCS3L_25,50,100_0003 Variable contrast, all orientations.eti'
    },
    'light': {
        'epd': 'M014_S001_SRCS3L_25,50,100_0004.epd',
        'eti': 'Results M014_S001_SRCS3L_25,50,100_0004 Variable contrast, all orientations.eti'
    }
}


class InitDataSetWithBurstsFlags:
    def __init__(self, data_dir, levels=['deep', 'light'], directory='filtered'):
        self.doas = []
        self.levels = levels
        self.directory = directory
        self.data_dir = data_dir
        self.run(directory)

    def run(self, directory):
        # data_dir = os.path.join('..', '..')
        data_dir = os.path.join(self.data_dir, 'data/', directory)
        sys.path.append(data_dir)

        for key, value in doa_info.items():
            if key in self.levels:
                doa_factory = CreateDOAWithBurstsFlags(data_dir, value['epd'], value['eti'], key)
                doa = doa_factory.create()
                self.doas.append(doa)

    def get_dataset_as_doas(self):
        return self.doas

    # TODO: Realize this when you have time
    # def serialize_doas(self, serialized_file_path):
    #     with open(serialized_file_path, 'w') as write_file:
    #         json.dump(obj={'doas': list(map(lambda x: x.to_json(), self.doas))}, fp=write_file)
    #
    # def deserialize_doas(self, serialized_file_path):
    #     with open(serialized_file_path) as json_file:
    #         data = json.load(json_file)
    #         return data