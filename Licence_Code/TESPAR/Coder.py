import numpy as np

from scipy.signal import find_peaks

from utils import Utils

# cutoff 1
maxD_allocate = 536
maxS_Allocate = 106


# cutoff 3
# maxD_allocate = 222
# maxS_Allocate = 48

class Coder:
    '''
    parameters:  - file_epd: - name of the file with extension .epd
    '''

    def __init__(self, doas):

        # self.ds_matrix = [[0 for i in range(maxS_Allocate)] for j in range(maxD_allocate)]
        self.ds_matrix = None

        self.channel_values = []
        self.maxD = -1
        self.maxS = -1

        self.aOffset = 0
        self.symbolic_array = []
        self.test_epoch = []

        # self.read_file()
        for doa in doas:
            doa_floats_list = Utils.obtain_floats_from_DOA(doa)
            self.channel_values.extend(doa_floats_list)

        self.set_matrix_dimensions()
        self.create_matrix()

    # def read_file(self):
    #     project_path = os.path.join('', '..')
    #     data_dir = os.path.join(project_path, self.filePath, '')
    #     sys.path.append(project_path)
    #
    #     for i in range(30):
    #         line = None
    #         file_name = "channel" + str(i) + ".txt"
    #         with open(os.path.join(data_dir, file_name), 'r') as f:
    #             line = f.readline()
    #             while line:
    #                 line = line.replace("[", "")
    #                 line = line.replace("]", "")
    #                 new_array = np.fromstring(line, dtype=np.float, sep=', ')
    #                 self.channel_values.append(new_array)
    #                 line = f.readline()

    def create_matrix(self):
        for channel in range(len(self.channel_values)):  # length 30*240
            d = 0
            s = 0
            current_epoch = 0
            last_zero_crossing = self.aOffset

            test_epoch = []
            markers_on = []

            length = len(self.channel_values[channel])
            # print("length = " + str(length))
            last_value = self.channel_values[channel][0]

            for i in range(1, length):
                # create array of every epoch

                if self.channel_values[channel][i] * last_value < 0:  # or i == length-1:  # Zero Crossing -> new Epoch

                    positive = self.channel_values[channel][i] > 0
                    d = i - last_zero_crossing

                    # print("the epoch")
                    # print(test_epoch)

                    # if i == length-1 and len(test_epoch) > 1:
                    #     test_epoch.append(self.channel_values[channel][i])
                    #     positive = not positive

                    if positive:
                        for j in range(len(test_epoch)):
                            test_epoch[j] = abs(test_epoch[j])

                    series = np.array(test_epoch)
                    peaks, _ = find_peaks(series)
                    mins, _ = find_peaks(series * -1)
                    x = np.linspace(0, 10, len(series))
                    # plt.plot(x, series, color='black');
                    # plt.plot(x[mins], series[mins], 'x', label='mins')
                    # plt.plot(x[peaks], series[peaks], '*', label='peaks')
                    # plt.legend()
                    # plt.ylim(-20, 20)
                    # plt.show()

                    s = len(mins)
                    self.ds_matrix[d][s] += 1

                    # if s > self.maxS:
                    #     self.maxS = s
                    # if d > self.maxD:
                    #     self.maxD = d
                    # print(s)
                    # print(d)
                    # plotul cu toate epocile

                    for j in range(len(mins)):
                        markers_on.append(mins[j] + last_zero_crossing)

                    test_epoch = []
                    test_epoch.append(self.channel_values[channel][i])
                    last_zero_crossing = i
                    current_epoch = current_epoch + 1
                    d = 0
                    s = 0
                else:
                    test_epoch.append(self.channel_values[channel][i])

                last_value = self.channel_values[channel][i]

    def set_matrix_dimensions(self):
        for channel in range(len(self.channel_values)):  # length 30*240
            d = 0
            s = 0
            current_epoch = 0
            last_zero_crossing = self.aOffset

            test_epoch = []

            length = len(self.channel_values[channel])
            last_value = self.channel_values[channel][0]

            for i in range(1, length):
                # create array of every epoch
                if self.channel_values[channel][i] * last_value < 0:  # or i == length-1:  # Zero Crossing -> new Epoch

                    positive = self.channel_values[channel][i] > 0
                    d = i - last_zero_crossing

                    if positive:
                        for j in range(len(test_epoch)):
                            test_epoch[j] = abs(test_epoch[j])

                    series = np.array(test_epoch)
                    peaks, _ = find_peaks(series)
                    mins, _ = find_peaks(series * -1)
                    x = np.linspace(0, 10, len(series))
                    s = len(mins)
                    # self.ds_matrix[d][s] += 1

                    if s > self.maxS:
                        self.maxS = s
                        print('update s: ' + str(s))
                    if d > self.maxD:
                        self.maxD = d
                        print('update d: ' + str(d))

                    test_epoch = []
                    test_epoch.append(self.channel_values[channel][i])
                    last_zero_crossing = i
                    current_epoch = current_epoch + 1
                    d = 0
                    s = 0
                else:
                    test_epoch.append(self.channel_values[channel][i])

                last_value = self.channel_values[channel][i]

        self.ds_matrix = [0 in range(self.maxS + 1) in range(self.maxD + 1)]
        print('find_matrix_dimensions  maxD: ' + str(self.maxD) + '  maxS: ' + str(self.maxS))
        # find_matrix_dimensions  maxD: 170  maxS: 28    // de ce printeaza astaaa  ?????
