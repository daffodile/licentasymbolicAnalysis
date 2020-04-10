import os

import numpy as np

from input_reader.MedataReaderBIN import MetadataReaderBIN
from input_reader.MetadataReaderEPD import MetadataReaderEPD
from input_reader.MetadataReaderETI import MetadataReaderETI
from models.Models import DOA
from models.Models import Channel
from models.Models import Trial
from models.Models import Segment


class CreateDOA:
    def __init__(self, data_dir, file_epd, file_eti, level):
        self.level = level
        self.data_dir = data_dir
        self.reader_epd = MetadataReaderEPD(data_dir, file_epd)
        self.reader_eti = MetadataReaderETI(data_dir, file_eti)
        self.codes_timestamps_reader = MetadataReaderBIN(data_dir, file_epd)
        self.doa = None

    def create(self):
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

            self.amplitude_array = self.amplitude[self.timestamp_array[0]:]

            channel_number = self.reader_epd.channel_info[i]
            channel = Channel(int(channel_number[len(channel_number) - 7:len(channel_number) - 4]))

            # for de 240 de iteratii
            for j in range(self.reader_eti.no_trials):
                if self.reader_eti.trials_description['Error'][j] != 1:
                    trial = Trial(self.reader_eti.trials_description['Trial'][j],
                                  self.reader_eti.trials_description['Condition'][j],
                                  self.reader_eti.trials_description['Contrast'][j],
                                  self.reader_eti.trials_description['Direction'][j],
                                  self.reader_eti.trials_description['Duration_us'][j],
                                  self.reader_eti.trials_description['Duration_f'][j])

                    timestamp_spontaneous = self.timestamp_array[4 * j]
                    code_spontaneous = self.codes_array[4 * j]

                    timestamp_stimulus = self.timestamp_array[4 * j + 1]
                    code_stimulus = self.codes_array[4 * j + 1]

                    timestamp_poststimulus = self.timestamp_array[4 * j + 2]
                    code_poststimulus = self.codes_array[4 * j + 2]

                    timestamp_end_poststimulus = self.timestamp_array[4 * j + 3]
                    code_end_poststimulus = self.codes_array[4 * j + 3]

                    seg_spontaneous = Segment(timestamp_spontaneous, timestamp_stimulus,
                                              code_spontaneous, code_stimulus)
                    # seg_spontaneous.set_values(self.amplitude[timestamp_spontaneous:timestamp_stimulus])
                    ind = timestamp_spontaneous
                    temp_amplitudes = []
                    while ind < timestamp_stimulus:
                        temp_amplitudes.append(self.amplitude[ind])
                        ind += 1
                    seg_spontaneous.set_values(temp_amplitudes)

                    trial.set_spontaneous(seg_spontaneous)

                    seg_stimulus = Segment(timestamp_stimulus, timestamp_poststimulus, code_stimulus, code_poststimulus)
                    # seg_stimulus.set_values(self.amplitude[timestamp_stimulus:timestamp_poststimulus])

                    ind = timestamp_stimulus
                    temp_amplitudes = []
                    while ind < timestamp_poststimulus:
                        temp_amplitudes.append(self.amplitude[ind])
                        ind += 1
                    seg_stimulus.set_values(temp_amplitudes)
                    trial.set_stimulus(seg_stimulus)

                    seg_poststimulus = Segment(timestamp_poststimulus, timestamp_end_poststimulus,
                                               code_poststimulus, code_end_poststimulus)
                    ind = timestamp_poststimulus
                    temp_amplitudes = []
                    while ind < timestamp_end_poststimulus:
                        temp_amplitudes.append(self.amplitude[ind])
                        ind += 1
                    seg_poststimulus.set_values(temp_amplitudes)
                    trial.set_poststimulus(seg_poststimulus)

                    channel.trials.append(trial)

            self.doa.channels.append(channel)

        return self.doa
