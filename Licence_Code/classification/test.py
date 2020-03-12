import numpy as np

from classification.RandomForest import RandomForest
from classification.SplitData import SplitData
from input_reader.InitDataSet import InitDataSet

initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()

#dataset, channels, levels, segment, orientation
# split_data = SplitData(doas, [1], ['light', 'deep'], ['spontaneous'], [90])
split_data = SplitData(doas, [1,2], ['light', 'deep'], ['spontaneous'], ['all'])



#what are you classifying?

# randomFClassifier = RandomForest(doas, 'deep/light', 'stimulus', 'none')
#
#
# doa_light = np.extract(condition=(lambda x: x.level == "light"), arr=doas)[0]
# doa_deep = np.extract(condition=(lambda x: x.level == "deep"), arr=doas)[1]
# doa_medium = np.extract(condition=(lambda x: x.level == "deep"), arr=doas)[2]
#
#
# random_forest = RandomForest(init_data.get_dataset_as_doas(), )
