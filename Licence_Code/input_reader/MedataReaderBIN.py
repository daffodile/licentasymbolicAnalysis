import os
import numpy as np

from input_reader.MetadataReaderEPD import MetadataReaderEPD


class MetadataReaderBIN:
    '''
    parameters:  - file_epd: - name of the file with extension .epd
    '''

    def __init__(self, path_epd, file_epd):
        self.path = path_epd
        self.metadata = MetadataReaderEPD(path_epd, file_epd)
        if (self.metadata.valid == False):
            return

        self.extract_event_codes_timestamps()

    '''
    Description: Reads all the values from the bin file
    '''

    def extract_event_codes_timestamps(self):
        with open(os.path.join(self.path, self.metadata.file_event_timestamps), 'rb') as timestamps_file, \
                open(os.path.join(self.path, self.metadata.file_event_codes), 'rb') as codes_file:
            timestamps_bytes = timestamps_file.read()
            codes_bytes = codes_file.read()

            self.event_codes = np.frombuffer(codes_bytes, dtype=np.int32)
            self.event_timestamps = np.frombuffer(timestamps_bytes, dtype=np.int32)

    def print_metadata(self):
        print('Timestamp  ', self.trial_timestamps)
        print('Coresponding code ', self.codes)
