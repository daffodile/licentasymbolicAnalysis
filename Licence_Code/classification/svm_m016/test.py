import os

'''
    SIMPLE TEST to check the vlaus in trials with the EEG
    test is passed
'''
from input_reader.InitDataSet import InitDataSet

data_dir = os.path.join('..', '..')

levels = ['deep6']
initialization_train = InitDataSet(current_directory=data_dir, subject_directory="m016", filtering_directory="classic",
                                   levels=levels)

doas = initialization_train.get_dataset_as_doas()

print('debug')
