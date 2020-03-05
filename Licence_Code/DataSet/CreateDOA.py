# Steps
# epd si eti - instantiation
# epd -> read bin files
import os

import numpy as np

from DataSet.MedataReaderBIN import MetadataReaderBIN
from DataSet.MetadataReaderEPD import MetadataReaderEPD
from DataSet.MetadataReaderETI import MetadataReaderETI
from DataSet.Models import DOA
from DataSet.Models import Channel
from DataSet.Models import Trial
from DataSet.Models import Segment


class CreateDOA:
    def __init__(self, data_dir, file_epd, file_eti, level):
        self.level = level
        self.data_dir = data_dir
        self.reader_epd = MetadataReaderEPD(data_dir, file_epd)
        self.reader_eti = MetadataReaderETI(data_dir, file_eti)
        self.codes_timestamps_reader = MetadataReaderBIN(data_dir, file_epd)
        self.doa = None

    def run(self):
        self.doa = DOA(self.level)
        self.amplitude_array = []
        self.timestamp_array = self.codes_timestamps_reader.event_timestamps
        self.codes_array = self.codes_timestamps_reader.event_codes

        # remove bad channels
        temp_channels_arr = []
        for i in range(len(self.reader_epd.channel_info)):
            if i + 1 not in self.reader_epd.bad_channels_arr:
                temp_channels_arr.append(self.reader_epd.channel_info[i])
        self.reader_epd.channel_info = temp_channels_arr

        # change the number of channels in epd file
        self.reader_epd.no_channels -= len(self.reader_epd.bad_channels_arr)

        # iterate over the channels
        for i in range(self.reader_epd.no_channels):

            with open(os.path.join(self.data_dir, self.reader_epd.channel_info[i].rstrip()),
                      'rb') as channel_info:
                values_of_channel = channel_info.read()

            # print(self.reader_epd.channel_info[i])
            self.amplitude = np.frombuffer(values_of_channel, dtype=np.float32)
            # print(self.timestamp_array)
            a1 = self.amplitude[self.timestamp_array[0]-1]
            a2 = self.amplitude[0]
            a3 = self.amplitude[self.timestamp_array[0]+1]
            self.amplitude_array = self.amplitude[self.timestamp_array[0]:]

            # print('channel' + str(i) + str(self.amplitude_array))

            channel = Channel(i + 1)

            trial_counter = 0
            for j in range(self.reader_eti.no_trials):
                if self.reader_eti.trials_description['Error'][j] != 1:
                    trial = Trial(self.reader_eti.trials_description['Trial'][j],
                                  self.reader_eti.trials_description['Condition'][j],
                                  self.reader_eti.trials_description['Contrast'][j],
                                  self.reader_eti.trials_description['Direction'][j],
                                  self.reader_eti.trials_description['Duration_us'][j],
                                  self.reader_eti.trials_description['Duration_f'][j])

                    contor = 0
                    for i in range(trial_counter, trial_counter + 3):
                        start_timestamp = self.timestamp_array[i]
                        end_timestamp = self.timestamp_array[i + 1]
                        start_code = self.codes_array[i]
                        end_code = self.codes_array[i + 1]
                        temp_amplitudes = []
                        j = start_timestamp

                        segment = Segment(start_timestamp, end_timestamp, start_code, end_code)

                        while j < end_timestamp:
                            temp_amplitudes.append(self.amplitude_array[contor])
                            j = j + 1
                            contor = contor + 1

                        segment.set_values(temp_amplitudes)
                        if start_code == 128:
                            trial.set_spontaneous(segment)

                        if start_code == 129:
                            trial.set_stimulus(segment)

                        if start_code == 150:
                            trial.set_poststimulus(segment)
                    trial_counter += 4
                    channel.trials.append(trial)
            self.doa.channels.append(channel)

