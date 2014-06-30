from abc import ABCMeta

class DatasetAdapter(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def createTrace(self):
        pass

    @abstractmethod
    def createInstance(self):
        pass

    @abstractmethod
    def createType(self);
        pass

    @abstractmethod
    def createSet(self):
        pass
