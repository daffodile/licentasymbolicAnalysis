# Steps
# epd si eti - instantiation
# epd -> read bin files
import json
import os
import sys

from DataSet.CreateDOA import CreateDOA
from DataSet.MedataReaderBIN import MetadataReaderBIN
from DataSet.MetadataReaderEPD import MetadataReaderEPD
from DataSet.MetadataReaderETI import MetadataReaderETI

data_dir = os.path.join('', '..')
data_dir = os.path.join(data_dir, 'Data', '')
sys.path.append(data_dir)

#  DEEP
file_epd_deep = 'M014_S001_SRCS3L_25,50,100_0002.epd'
file_eti_deep = "Results M014_S001_SRCS3L_25,50,100_0002 Variable contrast, all orientations.eti"

#MEDIUM
file_epd_medium = 'M014_S001_SRCS3L_25,50,100_0003.epd'
file_eti_medium = "Results M014_S001_SRCS3L_25,50,100_0003 Variable contrast, all orientations.eti"

#LIGHT
file_epd_light = 'M014_S001_SRCS3L_25,50,100_0004.epd'
file_eti_light = "Results M014_S001_SRCS3L_25,50,100_0004 Variable contrast, all orientations.eti"

class InitDataSet:
    def __init__(self):
        self.doas = []
        self.run()
        print(self.doas)

    def run(self):
        create_deep = CreateDOA(data_dir, file_epd_deep, file_eti_deep, 'deep')
        self.doas.append(create_deep.run())

        create_medium = CreateDOA(data_dir, file_epd_medium, file_eti_medium, 'medium')
        self.doas.append(create_medium.run())

        create_light = CreateDOA(data_dir, file_epd_light, file_eti_light, 'light')
        self.doas.append(create_light.run())

    # def seialize_doas(self, doas_file_name):
    #     with open('dataset.json', 'w') as write_file:
    #         json.dump(obj=self.doas.__dict__, fp=write_file, )
    #     json_data = json.dumps(self.doas.__dict__, lambda o: o.__dict__, indent=4)


