'''
Module for reading the metadata of the .eti file
'''

import sys
import os


class MetadataReaderETI:
    '''
    parameters: - path_eti: - path to the folder where the eti file is located
                - file_eti: - name of the file with extension .eti

    - first 5 fields are INT
    - last field is FLOAT
    --- we use this for conversion

    TODO: Rename the headers in eti
    From:
Trial,Contrast,Direction,Duration (us),Duration (frames),Error timing flag (1 if trial is compromised)
    To:
Trial,Condition,Contrast,Direction,Duration_us (us),Duration_f (frames),Error timing flag (1 if trial is compromised)
    '''

    def __init__(self, path_eti, file_eti):
        if file_eti[-3:] != 'eti':
            print('[{0}.{1}] {2} not a .eti file'.format(self.__class__.__name__, sys._getframe().f_code.co_name,
                                                         path_eti))
            self.valid = False
        else:
            self.dataset_path = path_eti
            self.eti_file = file_eti
            self.read_eti_metadata()
            self.valid = True

    '''
    Description: Reads all the information in the eti file
    '''

    def read_eti_metadata(self):
        lines = None
        with open(os.path.join(self.dataset_path, self.eti_file), 'r') as f:
            lines = f.readlines()

        # read the number of trials
        current_ofs = 0
        self.no_trials = int(lines[current_ofs].split(',')[1])

        # read the number of fields
        current_ofs += 1
        self.no_fields = int(lines[current_ofs].split(',')[1])

        # read the description fields names
        current_ofs += 2
        self.header_names = []
        self.header_names = lines[current_ofs].split(',')

        # read the description for each trial
        current_ofs += 1
        self.trials_description = {}
        for i in range(self.no_fields + 1):
            self.trials_description[self.header_names[i].split(' ')[0]] = []
        for i in range(0, self.no_trials):
            current_line = lines[current_ofs + i].rstrip()
            attributes = current_line.split(',')
            for j in range(self.no_fields - 1):
                if (j != 2 and j != 3):
                    attributes[j] = int(attributes[j])
                elif (j == 2):
                    attributes[j] = int(attributes[j].split(' ')[1])
                elif (j == 3):
                    attributes[j] = int(attributes[j].split(' ')[2])
            attributes[self.no_fields - 1] = float(attributes[self.no_fields - 1])
            if not attributes[self.no_fields]:
                attributes[self.no_fields] = 0
            else:
                attributes[self.no_fields] = int(attributes[self.no_fields])
            for j in range(self.no_fields + 1):
                oldValues = self.trials_description[self.header_names[j].split(' ')[0]]
                oldValues.append(attributes[j])
                tempDict = {self.header_names[j].split(' ')[0]: oldValues}
                self.trials_description.update(tempDict)

        print('[{0}.{1}] COMPLETE'.format(self.__class__.__name__, sys._getframe().f_code.co_name))

    def print_description(self):
        print('Number of trials ', self.no_trials)
        print('Number of fields ', self.no_fields)
        print('Header names ', self.header_names)
