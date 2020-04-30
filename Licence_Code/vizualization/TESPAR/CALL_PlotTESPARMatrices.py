from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
from utils.mark_bursts.MarkOutsiderWithBurstFlags_SeparateThresholds import mark_bursts_regions
from utils.mark_bursts.MarkOutsidersWithBurstsFlags import remove_bursted_trials_when_segment
from vizualization.TESPAR.PlotTESPARMatrices import get_channel_matrix_A, get_channel_trial_matrix_A

initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()

mark_bursts_regions(doas)

remove_bursted_trials_when_segment(doas)

encoding = Encoding('./../../data_to_be_saved/alphabet_3.txt')

good_channels = [2, 3, 4]
deep_trials = [5, 6, 11, 14]
medium_trials = [5, 6, 14]
light_trials = [8, 11, 14]
for i in range(len(good_channels)):
    for j in range(len(light_trials)):
        get_channel_trial_matrix_A(encoding, doas, 'light', good_channels[i], light_trials[j], log=False)
