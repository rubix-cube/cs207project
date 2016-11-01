import reprlib, numbers, collections
import math
from lazy import lazy
from SizedContainerTimeSeriesInterface import SizedContainerTimeSeriesInterface
import numpy as np

class TimeSeries(SizedContainerTimeSeriesInterface):
	"""
	TimeSeries class inherited from SizedContainerTimeSeriesInterface
	Underlying storage for time series are lists
	
	Attributes
	----------
	_time: list of numerics
		time component of our time series

	_value: list of numerics
		value component of our time series

	_timeseries: list of 2-tuples
		(time, value) pair representation of our time series

	Methods
	-------
	Most methods are inherited from SizedContainerTimeSeriesInterface, refer to SizedContainerTimeSeriesInterface for more details
	Subclass methods:
		values():
			Return value component as a numpy array

		times():
			Return time component as a numpy array

		items():
			Return list of (time, value) pairs as a numpy array

	"""
	

	def __init__(self, input_value, input_time = None):
		""" Constructor for time series
			
			Parameters
			----------
			input_value : sequence
				a sequence of data, must be numerics

			input_time : sequence, optional
				a sequence of time, must be numerics (datetime maybe supported in the future)

			Returns
			-------
			timeseries: TimeSeries
				a TimeSeries object
		"""

		if not isinstance(input_value, collections.Sequence):
			raise TypeError("Argument input_value must be Python sequence ")
		if input_time:
			if not isinstance(input_time, collections.Sequence):
				raise TypeError("Argument input_time must be Python sequence ")
			if len(input_time) != len(input_value):
				raise ValueError("Argument input_value must have same length with input_time")
			self._time = list(input_time)
		else:
			self._time = list(range(1, len(input_value) + 1))
		self._value = list(input_value)
		self._timeseries = list(zip(self._time, self._value))
		# self._dict = dict(zip(self._time), range(0, len(self._time)))

	def __getitem__(self, index):
		if isinstance(index, slice):
			# new_slice = slice(self._dict[index.start], self._dict[index.stop], index.step)
			return TimeSeries(self._value[index], self._time[index])
		if not isinstance(index, numbers.Integral):
			raise TypeError("Argument index must be either Python slice object or Python int")
		else:
			return self._timeseries[index]

	def __setitem__(self, index, value):
		if isinstance(index, numbers.Integral): 
		    self._value[index] = value
		    self._timeseries[index] = (self._time[index], value) 
		else:
		    raise TypeError('Index must be integers')
		#
		# if not isinstance(index, type(self._time[0])):
		# 	raise TypeError("Argument index must have same type as time item")
		# else:
		# 	self._value[self._dict[index]] = value
		# 	self._timeseries[self._dict[index]] = (value, index)


	# def __iter__(self):
	# 	for v in self._value:
	# 		yield v

	def times(self):
		return np.array(self._time)

	# def itertimes(self):
	# 	return iter(self._time)

	def values(self):
		return np.array(self._value)

	# def itervalues(self):
	# 	return iter(self._value)

	def items(self):
		return self._timeseries

	# def iteritems(self):
	# 	return iter(self._timeseries)


	def __add__(self, otherTS):
		# check otherTS type
		if not isinstance(otherTS, TimeSeries):
			raise TypeError('Can only add with time series')
		# check they have the same length and has equal time domain
		if len(self) != len(otherTS) or self._time != otherTS._time:
			raise ValueError(str(self)+' and '+ str(otherTS) + ' must have the same time points')
		return TimeSeries(list(map(lambda t: t[0] + t[1], zip(self._value, otherTS._value))), self._time)

	def __sub__(self, otherTS):
		# check otherTS type
		if not isinstance(otherTS, TimeSeries):
			raise TypeError('Can only subtract with time series')
		# check they have the same length and has equal time domain
		if len(self) != len(otherTS) or self._time != otherTS._time:
			raise ValueError(str(self) + ' and ' + str(otherTS) + ' must have the same time points')
		return TimeSeries(list(map(lambda t: t[0] - t[1], zip(self._value, otherTS._value))), self._time)


	def __eq__(self, otherTS):
		# check otherTS type
		if not isinstance(otherTS, TimeSeries):
			raise TypeError('Can only eval equal on time series')
		# check they have the same length and has equal time domain
		if len(self) != len(otherTS) or self._time != otherTS._time:
			raise ValueError(str(self) + ' and ' + str(otherTS) + ' must have the same time points')
		return self._timeseries == otherTS._timeseries


	def __mul__(self, otherTS):
		# check otherTS type
		if not isinstance(otherTS, TimeSeries):
			raise TypeError('Can only multiply with time series')
		# check they have the same length and has equal time domain
		if len(self) != len(otherTS) or self._time != otherTS._time:
			raise ValueError(str(self) + ' and ' + str(otherTS) + ' must have the same time points')
		return TimeSeries(list(map(lambda t: t[0] * t[1], zip(self._value, otherTS._value))), self._time)

	def __neg__(self):
		return TimeSeries([-v for v in self._value], self._time)

	def __pos__(self):
		return TimeSeries(self._value, self._time)

	@property
	def lazy(self):
		thunk = lazy(lambda x : x) #identity function
		return thunk(self)

@lazy
def check_length(a,b):
	return len(a) == len(b)

if __name__ == "__main__":
	t = check_length(TimeSeries(range(0,4), range(1,5)), TimeSeries(range(1,5), range(2,6)))
	# print(t.eval())
	x = TimeSeries(range(100),range(100))
	print(x == x.lazy.eval())
	
	t = TimeSeries([1,2,3], [0,5,10])
	print(t.interpolate([0,1,1.2]))
	print(t.interpolate([-100,100]))
	# t = check_length(TimeSeries(range(0,4), range(1,5)), TimeSeries(range(1,5), range(2,6)))
	# print(t.eval())
