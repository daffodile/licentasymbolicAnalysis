import os
import sys
import numpy as np

from DataSet.MedataReaderBIN import MetadataReaderBIN


class TrialExtractorEPD:

    def __init__(self, path_epd, file_epd):
        self.path = path_epd
        self.codes_timestamps_reader = MetadataReaderBIN(path_epd, file_epd)
        self.extract_trial()

    def extract_trial(self):
        self.amplitude_array = []
        self.timestamp_array = self.codes_timestamps_reader.event_timestamps
        self.codes_array = self.codes_timestamps_reader.event_codes

        self.storage = {128: [], 129: [], 150: []}
        # for i in range(len(self.codes_timestamps_reader.channel_files)):
        #     if i != 0 and i != 21 and i != 32:
        with open(os.path.join(self.path, self.codes_timestamps_reader.channel_files[2].rstrip()), 'rb') as channel_info:
          values_of_channel  = channel_info.read()
        self.amplitude = np.frombuffer(values_of_channel, dtype=np.float32)  # schimba cu float

        self.amplitude_array = self.amplitude[self.timestamp_array[0]-1:]

        contor = 0
        for i in range(len(self.timestamp_array)-1):
            start_timestamp = self.timestamp_array[i]
            end_timestamp = self.timestamp_array[i+1]
            start_code = self.codes_array[i]
            end_code = self.codes_array[i+1]
            temp_amplitudes = []
            j = start_timestamp

            while j < end_timestamp:
                temp_amplitudes.append(self.amplitude_array[contor])
                j = j+1
                contor = contor +1

            if start_code == 128:
                oldAmplitudes = self.storage[start_code]
                oldAmplitudes.append(temp_amplitudes)
                tempDict = {start_code: oldAmplitudes}
                self.storage.update(tempDict)

            if start_code == 129:
                oldAmplitudes = self.storage[start_code]
                oldAmplitudes.append(temp_amplitudes)
                tempDict = {start_code: oldAmplitudes}
                self.storage.update(tempDict)

            if start_code == 150:
                oldAmplitudes = self.storage[start_code]
                oldAmplitudes.append(temp_amplitudes)
                tempDict = {start_code: oldAmplitudes}
                self.storage.update(tempDict)

