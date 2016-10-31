from abc import ABCMeta, abstractmethod

class TimeSeriesInterface(metaclass = ABCMeta):
    
    @abstractmethod
    def __iter__(self):
        raise NotImplementedError('Concrete Implementation are missing for iter')

    