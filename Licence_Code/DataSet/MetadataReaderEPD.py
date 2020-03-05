'''
Module for reading the metadata of the .epd file
'''

import sys
import os

no_units_ofs = 5
metadata_window = 3


class MetadataReaderEPD:
    '''
    parameters: - path_epd: - path to the folder where the epd file is located
                - file_epd: - name of the file with extension .epd
    '''

    def __init__(self, path_epd, file_epd):
        if file_epd[-3:] != 'epd':
            print('[{0}.{1}] {2} not a .epd file'.format(self.__class__.__name__, sys._getframe().f_code.co_name,
                                                         path_epd))
            self.valid = False
        else:
            self.dataset_path = path_epd
            self.epd_file = file_epd
            self.read_epd_metadata()
            self.valid = True

    '''
    Description: Reads all the information in the epd file
    '''

    def read_epd_metadata(self):
        lines = None
        with open(os.path.join(self.dataset_path, self.epd_file), 'r') as f:
            lines = f.readlines()

        # read the number of channels
        current_ofs = no_units_ofs
        self.no_channels = int(lines[current_ofs])

        # read the sampling frequency
        current_ofs += metadata_window
        self.sampling_frequency = float(lines[current_ofs])

        # read the total number of samples
        current_ofs += metadata_window
        self.no_samples = int(lines[current_ofs])

        # read the filenames for each individual channel
        current_ofs += metadata_window
        self.channel_info = []
        for i in range(0, self.no_channels):
            self.channel_info.append(lines[current_ofs + i].rstrip())

        current_ofs += self.no_channels - 1
        # read name File holding event timestamps
        current_ofs += metadata_window
        self.file_event_timestamps = lines[current_ofs][:-1]
        #
        # read name File holding codes of events
        current_ofs += metadata_window
        self.file_event_codes = lines[current_ofs][:-1]

        # # read the number of events
        current_ofs += metadata_window
        self.no_events = int(lines[current_ofs])

        # # read the bad channels
        current_ofs += metadata_window + self.no_channels + 3 * metadata_window - 2
        self.bad_channels_arr = []
        self.bad_channels_arr = list(map(int,lines[current_ofs].split(',')))

        print('[{0}.{1}] COMPLETE'.format(self.__class__.__name__, sys._getframe().f_code.co_name))

    def print_metadata(self):
        print('Number of EEG channels ', self.no_channels)
        print('Sampling frequency ', self.sampling_frequency)
        print('Total number of samples ', self.no_samples)
        print('File holding event timestamps for the units, ', self.file_event_timestamps)
        print('File holding event codes for the units ', self.file_event_codes)
        print('Number of events ', self.no_events)
        print('Bad Channels ', self.bad_channels_arr)
