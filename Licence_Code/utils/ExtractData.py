import numpy as np

from input_reader.Models import DOA


class Result:

    def __init__(self):
        self.arrays = []


class NewData:

    def __init__(self, name, array, array_validate):
        self.name = name
        self.array_data = array
        self.array_validate = array_validate


class ExtractData:

    def __init__(self, doas, channels, levels, segment, orientation=['all']):
        # dataset
        self.doas = doas
        # features
        self.channels = channels
        self.levels = levels
        self.segment = segment
        self.orientation = orientation

        # functie care imi ia doar datele selectate based on features
        self.get_data()

    def get_data(self):

        self.result = Result()
        for j in range(len(self.doas)):
            if self.doas[j].level in self.levels:
                array = []
                array_validate = []
                for channel in self.doas[j].channels:
                    if channel.number in self.channels:
                        for trial in channel.trials:
                            if trial.direction in self.orientation or 'all' in self.orientation:
                                for segment in self.segment:
                                    # print('the segment is:' + segment)
                                    if segment == 'spontaneous':
                                        array.append(trial.spontaneous.values)
                                        array_validate.append(trial.spontaneous.values_outsiders)
                                    if segment == 'stimulus':
                                        array.append(trial.stimulus.values)
                                        array_validate.append(trial.stimulus.values_outsiders)
                                    if segment == 'poststimulus':
                                        array.append(trial.poststimulus.values)
                                        array_validate.append(trial.poststimulus.values_outsiders)

                array_final = NewData(self.doas[j].level, array, array_validate)
                self.result.arrays.append(array_final)

        # print(self.result)
        return self.result

    def get_data_2matrices_test(self):

        self.result = Result()
        for j in range(len(self.doas)):
            if self.doas[j].level in self.levels:
                array = []
                array_validate = []
                for channel in self.doas[j].channels:
                    if channel.number in self.channels:
                        for trial in channel.trials:
                            if trial.direction in self.orientation or 'all' in self.orientation:
                                values_temp = []
                                validations_temp = []
                                for segment in self.segment:
                                    # print('the segment is:' + segment)
                                    if segment == 'spontaneous':
                                        values_temp.extend(trial.spontaneous.values)
                                        validations_temp.extend(trial.spontaneous.values_outsiders)
                                    if segment == 'stimulus':
                                        values_temp.extend(trial.stimulus.values)
                                        validations_temp.extend(trial.stimulus.values_outsiders)
                                    if segment == 'poststimulus':
                                        values_temp.extend(trial.poststimulus.values)
                                        validations_temp.extend(trial.poststimulus.values_outsiders)
                                array.append(values_temp)
                                array_validate.append(validations_temp)
                array_final = NewData(self.doas[j].level, array, array_validate)
                self.result.arrays.append(array_final)

        # print(self.result)
        return self.result