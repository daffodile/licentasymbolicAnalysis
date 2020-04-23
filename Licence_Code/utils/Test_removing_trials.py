import os

from input_reader.InitDataSetWithBurstsFlags import InitDataSetWithBurstsFlags
from utils.MarkOutsiderWithBurstFlags_SeparateThresholds import mark_bursts_regions
from utils.MarkOutsidersWithBurstsFlags import remove_bursted_trials_when_segment

data_dir = os.path.join('', '..')
initialization = InitDataSetWithBurstsFlags(data_dir, levels=['deep', 'medium', 'light'])
doas = initialization.get_dataset_as_doas()

print('do not expand left right')

thresholds = {2: 23.263285, 3: 22.366724, 4: 27.422037, 5: 22.331213, 6: 23.394754, 7: 22.354338, 8: 27.749441,
              9: 29.266874, 10: 22.621815, 11: 22.75086, 12: 22.371376, 13: 21.829714, 14: 27.50188, 15: 23.687954,
              16: 29.949093, 17: 25.198391, 18: 32.699684, 19: 25.501558, 20: 21.380661, 21: 25.648182, 23: 25.984198,
              24: 26.205786, 25: 25.768787, 26: 20.381828, 27: 25.502258, 28: 20.292067, 29: 25.598713, 30: 27.259365,
              31: 25.049229, 32: 30.300776}

mark_bursts_regions(doas, thresholds=thresholds)
# mark_bursts_regions(doas)
remove_bursted_trials_when_segment(doas, tolerance_inside_trial=0.5)

'''
run with threshold/ channel that are converged 0.33 tolerance
~ 140 deep, 78 medium, 27 light

same converged trials, tolerance 0.5
deep 206, medium 140, light 73

first threshold met per channel tolerance 0.33
deep 181, medium 123, light 80

first thresold met per channel, tolerance 0.5
deep 216, medium 191, light 147
'''
