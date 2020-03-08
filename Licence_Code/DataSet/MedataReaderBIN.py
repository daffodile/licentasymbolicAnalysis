import sys
import os
import numpy as np

from DataSet.MetadataReaderEPD import MetadataReaderEPD


class MetadataReaderBIN:
    '''
    parameters:  - file_epd: - name of the file with extension .epd
    '''

    def __init__(self, path_epd, file_epd):
        # print("ASHGDABSJDAN: " + os.getcwd())
        # project_path = os.path.join('..', '..')
        # data_dir = os.path.join(project_path, 'Data', 'data')
        # sys.path.append(project_path)
        # print('Project path: ' + data_dir)
        self.path = path_epd
        self.metadata = MetadataReaderEPD(path_epd, file_epd)
        if (self.metadata.valid == False):
            return

        self.extract_event_codes_timestamps()

    '''
    Description: Reads all the values from the bin file
    '''

    def extract_event_codes_timestamps(self):
        lines = None
        self.channel_info = self.metadata.channel_info
        with open(os.path.join(self.path, self.metadata.file_event_timestamps), 'rb') as timestamps_file, \
                open(os.path.join(self.path, self.metadata.file_event_codes), 'rb') as codes_file:
            # read the code of the trial and it's coresponding timestamp
            # for i in range(self.metadata.no_events):

            timestamps_bytes = timestamps_file.read()

            codes_bytes = codes_file.read()

            self.event_codes = np.frombuffer(codes_bytes, dtype=np.int32)

            self.event_timestamps = np.frombuffer(timestamps_bytes, dtype=np.int32)

            # make structured array from the timestamps
            trial_type = [('start', np.int32), ('on', np.int32), ('off', np.int32), ('end', np.int32)]
            # self.trial_timestamps = event_timestamps.view(trial_type)

            # print('[{0}.{1}] COMPLETE - Timestamps RAW {2}(first trial) - Unique Codes of Events {3}'\
            # .format(self.__class__.__name__, sys._getframe().f_code.co_name, event_timestamps[:4], np.unique(self.event_codes)))

    def print_metadata(self):
        print('Timestamp  ', self.trial_timestamps)
        print('Coresponding code ', self.codes)
