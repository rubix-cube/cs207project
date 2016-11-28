import numpy as np
import reprlib, numbers, collections
import math
from timeseries.SizedContainerTimeSeriesInterface import SizedContainerTimeSeriesInterface


class ArrayTimeSeries(SizedContainerTimeSeriesInterface):
    """ 
    ArrayTimeSeries class, inherited form SizedContainerTimeSeriesInterface
    Underlying storage are numpy arrays rather than lists

    Attributes
    ----------
    _time: numpy array of numerics
        time component of our time series

    _value: numpy array of numerics
        value component of our time series

    _timeseries: numpy array of 2-tuples
        [time, value] pair representation of our time series

    Methods
    -------
    Methods are inherited from SizedContainerTimeSeriesInterface, refer to SizedContainerTimeSeriesInterface for more details

    """ 
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
            return ArrayTimeSeries(list(self._time[index]), list(self._value[index]))
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

    def times(self):
        return self._time

    def values(self):
        return self._value

    def items(self):
        return list(self._timeseries)

    def interpolate(self, newTimes):
        newValues = []
        time, value = self._time, self._value
        counter, n = 1, len(time)
        for t in newTimes:
            while counter < n:
                if t < time[0]:
                    newValues.append(value[0])
                    break
                elif t > time[n-1]:
                    newValues.append(value[n-1])
                    break
                elif time[counter-1] <= t <= time[counter]:
                    # newVal = t + t * ((value[counter]-value[counter-1]) / (time[counter] - time[counter-1]))
                    # t-time[counter-1] * value[counter]-value[counter-1]
                    newVal = ((value[counter]-value[counter-1])/(time[counter]-time[counter-1]))*(t-time[counter-1]) + value[counter-1]
                    newValues.append(newVal)
                    break
                else:
                    counter += 1
        return ArrayTimeSeries(newTimes, newValues)


    def __add__(self, otherTS):
        # check otherTS type
        if not isinstance(otherTS, ArrayTimeSeries):
            raise TypeError('Can only add with time series')
        # check they have the same length and has equal time domain
        if len(self) != len(otherTS) or np.any(self._time != otherTS._time):
            raise ValueError(str(self)+' and '+ str(otherTS) + ' must have the same time points')
        return ArrayTimeSeries(self._time, self._value + otherTS._value)

    def addConst(self, num):
        return ArrayTimeSeries(self._time, self._value + num)

    def __sub__(self, otherTS):
        # check otherTS type
        if not isinstance(otherTS, ArrayTimeSeries):
            raise TypeError('Can only subtract with time series')
        # check they have the same length and has equal time domain
        if len(self) != len(otherTS) or np.any(self._time != otherTS._time):
            raise ValueError(str(self) + ' and ' + str(otherTS) + ' must have the same time points')
        return ArrayTimeSeries(self._time, self._value - otherTS._value)


    def subConst(self, num):
        return ArrayTimeSeries(self._time, self._value - num)

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

    def multConst(self, num):
        return ArrayTimeSeries(self._time, self._value * num)

    def __neg__(self):
        return ArrayTimeSeries(self._time, - self._value)

    def __pos__(self):
        return ArrayTimeSeries(self._time, self._value)

    
