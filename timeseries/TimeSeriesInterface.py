from abc import ABCMeta, abstractmethod

class TimeSeriesInterface(metaclass = ABCMeta):
    """
    Interface for time series class

    """
    
    @abstractmethod
    def __iter__(self):
        raise NotImplementedError('Concrete Implementation are missing for iter')

    @abstractmethod
    def __str__(self):
        return "This is the TimeSeriesInterface, implement it in subclasses"

    @abstractmethod
    def __repr__(self):
        return "This is the TimeSeriesInterface, implement it in subclasses"    	
