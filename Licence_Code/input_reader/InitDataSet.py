import json
import ast
import os
import sys

'''
structure of the datasets:

data -> m014: raw 
            classic :   one .epd file per condition  - identify all the binary files
                        one .eti file per condition  - reading details about trials
                        one .csv file per condition // we do not read it for now (29/04/2020)
                        one Event-Timestamps.bin file per condition - identifying trials in time
                        one Event-Codes.bin file per condition - identifying segments
                        33 binary files of the recording per condition
                        doa_info.txt containing a dictionary 
                                key = condition name
                                values = .eti, .epd files for the condition
                        filters.txt - optional file, describes the filters that have been applied to this version
                                    of the dataset
                                    - all mentioned filters were applied for each condition individually
'''
from input_reader.CreateDOA import CreateDOA


class InitDataSet:
    def __init__(self, current_directory, subject_directory, filtering_directory, levels=['deep', 'medium', 'light'],
                 trials_to_skip=None):
        '''

        :param current_directory: path from the parent directory of the calling file up to the root directory of 'data'
        :param subject_directory: which subject to choose 'm014', 'm015'
        :param filtering_directory: name of the filtering status: 'raw', 'classic', 'highpass10'
        :param levels: which conditions to be fetched to form tha dataset: 'deep1', 'deep2', 'medium3', 'light4', 'medium5'
        :param trials_to_skip: if there are manually annotated trials in the .eti file, else ignore
        '''
        if trials_to_skip is None:
            trials_to_skip = []
        self.doas = []
        self.levels = levels
        self.trials_to_skip = trials_to_skip

        # create the directories structure
        data_dir = os.path.join(current_directory, 'data/')
        data_dir = os.path.join(data_dir, subject_directory)
        data_dir = os.path.join(data_dir, filtering_directory)
        self.data_dir = data_dir
        sys.path.append(data_dir)
        self.run()

    def run(self):
        # get the dictionary that keep conditions files
        doa_file = self.data_dir + '/doa_info.txt'
        with open(doa_file, 'r') as f:
            # with open('doa_info.txt', 'r') as f:
            s = f.read()
            doa_info = ast.literal_eval(s)

        for key, value in doa_info.items():
            if key in self.levels:
                doa_factory = CreateDOA(self.data_dir, value['epd'], value['eti'], key)
                doa = doa_factory.create(self.trials_to_skip)
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
