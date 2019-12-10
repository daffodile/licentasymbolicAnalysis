from enum import Enum


class SegmentLabel(Enum):
    SPONTANEOUS = 1
    STIMULUS = 2
    POST_STIMULUS = 3


class ClassLabel(Enum):
    LIGHT = 1
    MEDIUM = 2
    DEEP = 3


class Segment:
    def __init__(self, ClassLabel, SegmentLabel, channel_number, sample_array):
        self.class_label = ClassLabel
        self.segment_label = SegmentLabel
        self.channel_number = channel_number
        self.sample_array = sample_array
