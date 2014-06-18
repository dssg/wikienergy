#!/usr/bin/python
from abc import ABCMeta

class DeviceInstance(object):
    '''DeviceInstance

    Attributes:
        data -- a timeseries of measurements in a pandas dataframe
        params -- a dict of parameters representing this instance of a device
    '''
    __metaclass__ = ABCMeta

    def __init__(self, traces=[], params={}):
        self.traces = traces
        self.params = params

    def get_parameters(self):
        return self.params

    def get_traces(self):
        return self.traces

    @abstractmethod
    def learn_parameters(self):
        # procedure to learn parameters a specific device
        pass

    def set_parameters(self, params):
        # replaces old parameters with manually updated parameters
        self.params = params

    def set_traces(self, traces):
        # replaces traces
        self.data = data

class DeviceType(object):
    '''DeviceType models the general parameters for a set of devices

    Attributes:
        devices -- list of devices in the device set
        name    -- name of the device type
        params  -- set of parameters used to model the device
    '''
    # TODO - figure out how to store data efficiently
    __metaclass__ = ABCMeta

    def __init__(self, devices=[], name=None, params={}):
        self.devices = devices
        self.name = name
        self.params = params

    @abstractmethod
    def generate_data(self, timeframe):
        # generates generic data for this device within a given timeframe
        pass

    def get_devices(self):
        return self.devices

    def get_name(self):
        return self.name

    def get_parameters(self):
        return self.params

    @abstractmethod
    def learn_parameters(self):
        pass

    @abstractmethod
    def probability_present(self, aggregated_data):
        # evaluates the probability of being present in a particular timeseries
        pass

    def set_devices(self, devices):
        self.devices = devices

    def set_name(self, name):
        self.name = name

    def set_parameters(self, params):
        self.params = params

class MeteredUnit(object):
    '''Class to represent a metered with known (or unknown) device types
    '''

    def __init__(self, device_types=[], params={}):
        self.device_types = device_types

    def get_device_types(self):
        return self.device_types

    def get_parameters(self):
        return self.params

    @abstractmethod
    def learn_device_types(self, data, possible_device_types):
        # learns which devices are present, retains and returns the devices
        # which are.
        pass

    @abstractmethod
    def learn_disaggregator_parameters(self, timeframe=None):
        pass

    @abstractmethod
    def disaggregate(self, aggregated_data):
        # takes in unlabeled data, returns labeled data
        disaggregated_data = None
        confidences = None
        return disaggregated_data, confidences

    def set_device_types(self, device_types):
        self.device_types = device_types

    def set_parameters(self, params):
        self.params = params

class Error(Exception):
    '''Base class for exceptions in this module.'''
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)

class DatasetError(Error):
    '''Exception raised for errors in the dataset.

    Attributes:
        msg  -- explanation of the error
    '''
    pass

class UndefinedDeviceClassesError(Error):
    '''Exception raised for errors in the dataset.

    Attributes:
        msg  -- explanation of the error
    '''
    pass
