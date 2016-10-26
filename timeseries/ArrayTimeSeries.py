import numpy as np
import reprlib, numbers, collections
import math
from TimeSeries import TimeSeries 


class ArrayTimeSeries(TimeSeries):

    def __init__(self, input_value, input_time):
        if not isinstance(input_value, collections.Sequence):
            raise TypeError("Argument input_value must be Python sequence ")
        if not isinstance(input_time, collections.Sequence):
            raise TypeError("Argument input_time must be Python sequence ")
        if len(input_time) != len(input_value):
            raise ValueError("Argument input_value must have same length with input_time")
        self._time = np.array(input_time)
        self._value = np.array(input_value)
        self._timeseries = np.array(list(zip(self._time, self._value)))
        #self._dict = dict(zip(self._time), range(0, len(self._time)))


    def __getitem__(self, index):
        if isinstance(index, slice):
        # new_slice = slice(self._dict[index.start], self._dict[index.stop], index.step)
            return TimeSeries(list(self._value[index]), list(self._time[index]))
        if not isinstance(index, numbers.Integral):
            raise TypeError("Argument index must be either Python slice object or Python int")
        else:
            return self._timeseries[index]


    def __setitem__(self, index, value):
        if isinstance(index, numbers.Integral): 
            self._value[index] = value
            self._timeseries[index][1] = value
        else:
            raise TypeError('Index must be integers')


    def __len__(self):
        return len(self._value)

    def __iter__(self):
        """returns values

        """
        for t in self._value:
            yield t


    def itertimes(self): 
        """returns times
        """
        for v in self._time:
            yield v
        
    def iteritems(self):
        """returns k/v tuples

        """
        for v in self._timeseries:
            yield v
    
