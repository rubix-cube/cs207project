import numpy as np
import reprlib, numbers, collections
import math
from SizedContainerTimeSeriesInterface import SizedContainerTimeSeriesInterface


class ArrayTimeSeries(SizedContainerTimeSeriesInterface):

    def __init__(self, input_time, input_value):
        if not isinstance(input_value, collections.Sequence) and not isinstance(input_value, np.ndarray):
            raise TypeError("Argument input_value must be Python sequence ")
        if not isinstance(input_time, collections.Sequence) and not isinstance(input_value, np.ndarray):
            raise TypeError("Argument input_time must be Python sequence ")
        if len(input_time) != len(input_value):
            raise ValueError("Argument input_value must have same length with input_time")
        self._time = np.array(input_time)
        self._value = np.array(input_value)
        self._timeseries = np.array(list(zip(self._time, self._value)))


    def __getitem__(self, index):
        if isinstance(index, slice):
            return (TimeSeries(list(self._time[index]), list(self._value[index])))._timeseries
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

    def itervalues(self):
        for v in self._value:
            yield v

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


    def __add__(self, otherTS):
        # check otherTS type
        if not isinstance(otherTS, ArrayTimeSeries):
            raise TypeError('Can only add with time series')
        # check they have the same length and has equal time domain
        if len(self) != len(otherTS) or np.any(self._time != otherTS._time):
            raise ValueError(str(self)+' and '+ str(otherTS) + ' must have the same time points')
        return ArrayTimeSeries(self._time, self._value + otherTS._value)

    def __sub__(self, otherTS):
        # check otherTS type
        if not isinstance(otherTS, ArrayTimeSeries):
            raise TypeError('Can only subtract with time series')
        # check they have the same length and has equal time domain
        if len(self) != len(otherTS) or np.any(self._time != otherTS._time):
            raise ValueError(str(self) + ' and ' + str(otherTS) + ' must have the same time points')
        return ArrayTimeSeries(self._time, self._value - otherTS._value)


    def __eq__(self, otherTS):
        # check otherTS type
        if not isinstance(otherTS, ArrayTimeSeries):
            raise TypeError('Can only eval equal on time series')
        # check they have the same length and has equal time domain
        if len(self) != len(otherTS) or np.any(self._time != otherTS._time):
            raise ValueError(str(self) + ' and ' + str(otherTS) + ' must have the same time points')
        return np.all(self._value == otherTS._value)


    def __mul__(self, otherTS):
        # check otherTS type
        if not isinstance(otherTS, ArrayTimeSeries):
            raise TypeError('Can only multiply with time series')
        # check they have the same length and has equal time domain
        if len(self) != len(otherTS) or np.any(self._time != otherTS._time):
            raise ValueError(str(self) + ' and ' + str(otherTS) + ' must have the same time points')
        return ArrayTimeSeries(self._time, self._value * otherTS._value)

    def __neg__(self):
        return ArrayTimeSeries(self._time, - self._value)

    def __pos__(self):
        return ArrayTimeSeries(self._time, self._value)

    
