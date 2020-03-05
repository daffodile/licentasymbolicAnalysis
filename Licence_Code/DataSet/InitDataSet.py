# Steps
# epd si eti - instantiation
# epd -> read bin files
from DataSet.MedataReaderBIN import MetadataReaderBIN
from DataSet.MetadataReaderEPD import MetadataReaderEPD
from DataSet.MetadataReaderETI import MetadataReaderETI

#
# class InitDataSet:
#     def __init__(self, data_dir, file_epd, file_eti):
#         self.reader_epd = MetadataReaderEPD(data_dir, file_epd)
#         self.reader_eti = MetadataReaderETI(data_dir, file_eti)
#         self.codes_timestamps_reader = MetadataReaderBIN(data_dir, file_epd)
#
#     def run(self):
#