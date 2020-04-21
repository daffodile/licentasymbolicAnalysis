
from input_reader.InitDataSet import InitDataSet
from utils.mark_bursts.MarkOutsiderWithBurstFlags_SeparateThresholds import mark_bursts_regions
from utils.mark_bursts.MarkOutsidersWithBurstsFlags import remove_bursted_trials_when_segment
from utils.mark_bursts.MarkOutsidersWithBurstsFlags_OneThreshold import mark_bursts_regions_one_threshold

initialization = InitDataSet(levels=['deep', 'medium', 'light'])
doas = initialization.get_dataset_as_doas()

# first original method with 2*std_dev
# mark_outsiders(doas, max_interbursts_dist=200)

print('do not expand left right')

# SAU 1 SAU 2
#  1 th
mark_bursts_regions_one_threshold(doas)

# diff th
mark_bursts_regions(doas)

remove_bursted_trials_when_segment(doas)

'''
    here run with overall threshold from full dataset, 19.94

remove_bursted_trials_when_full_trial(doas)

run as it is: th 19.94, interbursts 364, NO expansion
output 
[2, 6, 7, 13, 14, 15, 16, 18, 19, 20, 22, 24, 25, 29, 33, 34, 35, 39, 42, 45, 47, 48, 49, 55, 60, 61, 62, 63, 68, 73, 75, 80, 86, 89, 94, 95, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 113, 114, 115, 116, 118, 119, 120, 122, 124, 126, 127, 129, 130, 132, 133, 135, 137, 143, 144, 147, 149, 154, 157, 160, 161, 162, 164, 166, 171, 173, 175, 178, 182, 192, 193, 195, 196, 204, 211, 214, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 235, 236, 239]
deep in a channel there are 135 trials left
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 67, 69, 71, 72, 73, 74, 76, 78, 79, 80, 81, 83, 84, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 186, 187, 189, 190, 191, 192, 193, 194, 195, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240]
light in a channel there are 15 trials left

'''
