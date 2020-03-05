class DOA:
    def __init__(self, level):
        self.level = level
        self.channels = []


class Channel:
    def __init__(self, number):
        self.number = number
        self.trials = []


class Trial:
    def __init__(self, trial_number, condition, contrast, direction, duration_us, duration_f):
        self.trial_number = trial_number
        self.condition = condition
        self.contrast = contrast
        self.direction = direction
        self.duration_us = duration_us
        self.duration_f = duration_f
        self.spontaneous = None
        self.stimulus = None
        self.poststimulus = None

    def set_spontaneous(self, segment):
        self.spontaneous = segment

    def set_stimulus(self, segment):
        self.stimulus = segment

    def set_poststimulus(self, segment):
        self.poststimulus = segment


class Segment:
    def __init__(self, start_time, end_time, start_code, end_code):
        self.start_time = start_time
        self.end_time = end_time
        self.start_code = start_code
        self.end_code = end_code
        self.values = []

    def set_values(self, float_arr):
        self.values = float_arr
