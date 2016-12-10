from abc import ABCMeta, abstractmethod

class TimeSeriesInterface(metaclass = ABCMeta):
    """
    Interface for time series class
    Subclasses should support iteration over time series

    Methods
    -------
    __iter__():
        Returns an iterator or a generator that enables iteration through our time series

    __str__():
        String representations of our time series

    __repr__():
        String representations of our time series        

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
  	
