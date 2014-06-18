#!/usr/bin/python
from disaggregator import DeviceInstance, DeviceType, MeteringUnit

class HMMDeviceInstance(DeviceInstance):
    '''HMMDeviceInstance'''

    def learn_parameters(self):
        pass
class HMMDeviceType(DeviceType):
    '''HMMDeviceInstance'''

    def generate_data(self, timeframe):
        pass

    def learn_parameters(self):
        pass

    def probability_present(self, aggregated_data):
        pass

class HMMMeteringUnit(MeteringUnit):
    '''HMMDeviceInstance'''

    def learn_device_types(self, data, possible_device_types):
        pass

    def learn_disaggregator_parameters(self, timeframe=None):
        pass

    def disaggregate(self, aggregated_data):
        disaggregated_data = None
        confidences = None
        return disaggregated_data, confidences
