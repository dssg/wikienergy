#!/usr/bin/python
import pandas as pd

class DeviceInstance:
    '''DeviceInstance

    Attributes:
        data -- a timeseries of measurements in a pandas dataframe
        params -- a dict of parameters representing this instance of a device
    '''
    # TODO - figure out how to store data efficiently

    def __init__(self, traces=[], params={}):
        self.traces = traces
        self.params = params

    def add_traces(self, traces):
        # adds new traces to set of old traces
        pass

    def get_traces(self):
        return self.traces

    def get_parameters(self):
        return params

    def learn_parameters(self):
        # procedure to learn parameters a specific device
        pass

    def update_traces(self, traces):
        # replaces traces
        self.data = data

    def update_parameters(self,params):
        # replaces old parameters with manually updated parameters
        self.params = params

class DeviceType:
    '''DeviceType models the general parameters for a set of devices

    Attributes:
        devices -- list of devices in the device set
        name    -- name of the device type
        params  -- set of parameters used to model the device
    '''
    # TODO - figure out how to store data efficiently

    def __init__(self, devices=[], name=None, params=None):
        self.devices = devices
        self.name = name

    def add_devices(self, devices):
        self.devices += devices

    def generate_data(self,timeframe):
        # generates generic data for this device in a given timeframe
        pass

    def get_devices(self):
        return devices

    def get_parameters(self):
        return params

    def learn_parameters(self):
        pass

    def probability_present(self, data):
        # evaluates the probability of being present in a particular dataset
        pass

    def update_devices(self, devices):
        self.devices = devices

    def update_name(self, name):
        self.name = name

    def update_parameters(self, params):
        # manually updates parameters
        self.params = params

class MeteredUnit:
    '''Class to represent a metered with known (or unknown) device types
    '''

    def __init__(self, device_types=[]):
        self.device_types = device_types

    def add_device_types(self):
        pass

    def get_device_types(self):
        return self.device_types

    def learn_device_types(self, data, possible_device_types):
        # learns which devices are present, retains and returns the devices
        # which are.
        pass

    def learn_disaggregator_parameters(self,timeframe=None):
        pass

    def disaggregate(self, data):
        # gets unlabeled data, returns labeled data
        disaggregated_data = None
        confidences = None
        return disaggregated_data, confidences

    def update_device_types(self, device_types):
        self.device_types = device_types


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
