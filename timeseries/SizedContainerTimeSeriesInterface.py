from TimeSeriesInterface import TimeSeriesInterface
from abc import abstractmethod, ABCMeta
import numpy as numpy
import math

class SizedContainerTimeSeriesInterface(TimeSeriesInterface):
	"""
	Interface for time series classes which should support Sized operations(__len__) and Container operations(__contains__)
	Subclasses should also support iteration and arithmetic operations.

	Methods
	-------
	Common sequence operations: 
		__getitem__(index):
			Get a (time, value) tuple at 'index' in our time series (index can be a slice object, in which case we get a new TimeSeries object)

		__setitem__(index, value):
			Set the value of the (time, value) tupe at 'index' in our times series (index can only be a integer)

		__len__():
			Get the length of our time series

	Iterations over time series:
		__iter__():
			A generator function yielding the value component of our time series

		itervalues():
			Return a iterator to the value component of our time series
		
		itertimes():
			Return a iterator to the time component of our time series

		iteritems():
			Return a iterator to the list of (time, value) tuple

	Arithmetic operations:
		__add__(otherTimeSeries):
			Return a new TimeSeries object whose value is the component-wise addition of the value of our time series and the value of otherTimeSeries
			otherTimeSeries must have exactly the same time component with our time series

		__sub__(otherTimeSeries):
			Return a new TimeSeries object whose value is the component-wise difference of the value of our time series and the value of otherTimeSeries
			otherTimeSeries must have exactly the same time component with our time series

		__mul__(otherTimeSeries):
			Return a new TimeSeries object whose value is the component-wise product of the value of our time series and the value of otherTimeSeries
			otherTimeSeries must have exactly the same time component with our time series

		__eq__(otherTimeSeries):
			Return True if both time and value components of our time series are exactly the same with those of otherTimeSeries

		__neg__():
			Return a new TimeSeries object whose value is the component-wise negation of the value of our time series

		__pos__():
			Return a new TimeSeries object which is identical to our time series

		__abs__():
			Return the 2-norm of the value component of our time series
		
		__bool__():
			True if the 2-norm of the value component of our time series is greater than 0, False otherwise

		interpolate(times):
			Return a new TimeSeries object with times given and newly computed values which are linearly interpolated using orginal time series
			The times passed in should be in ascending order

	"""

	def __len__(self):
		return len(self._value)

	@abstractmethod
	def __getitem__(self, index):
		raise NotImplementedError('Concrete Implementation are missing for __getitem__')

	@abstractmethod
	def __setitem__(self, index, value):
		raise NotImplementedError('Concrete Implementation are missing for __setitem__')


	def __iter__(self):
		# raise NotImplementedError('Concrete Implementation are missing for __iter__')
		for v in self._value:
			yield v

	def itertimes(self):
		# raise NotImplementedError('Concrete Implementation are missing for itertimes')
		return iter(self._time)

	def itervalues(self):
		# raise NotImplementedError('Concrete Implementation are missing for itervalues')
		return iter(self._value)

	def iteritems(self):
		# raise NotImplementedError('Concrete Implementation are missing for iteritems')
		return iter(self._timeseries)

	@abstractmethod
	def __add__(self, otherTS):
		raise NotImplementedError('Concrete Implementation are missing for __add__')

	@abstractmethod
	def __sub__(self, otherTS):
		raise NotImplementedError('Concrete Implementation are missing for __sub__')

	@abstractmethod
	def __eq__(self, otherTS):
		raise NotImplementedError('Concrete Implementation are missing for __eq__')

	@abstractmethod
	def __mul__(self, otherTS):
		raise NotImplementedError('Concrete Implementation are missing for __mul__')

	@abstractmethod
	def __neg__(self):
		raise NotImplementedError('Concrete Implementation are missing for __neg__')

	@abstractmethod
	def __pos__(self):
		raise NotImplementedError('Concrete Implementation are missing for __pos__')

	def __contains__(self):
		return value in self._value 	

	def __abs__(self):
		return math.sqrt(sum(x * x for x in self))

	def __bool__(self):
		return bool(abs(self))

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
					newVal = t + t * ((value[counter]-value[counter-1]) / (time[counter] - time[counter-1]))
					newValues.append(newVal)
					break
				else:
					counter += 1
		return TimeSeries(newValues, newTimes)

	def __repr__(self):
		#return 'TimeSeries({})'.format([i for i in self._timeseries])
		'''
		if len(self._timeseries) > 10:
			return 'TimeSeries(['+','.join('{}'.format(i) for i in self._timeseries[:5])\
					+ '...'+','.join('{}'.format(i) for i in self._timeseries[-5:]) + '])'\
					+ ' -- omitting {} objects'.format(len(self._timeseries) - 10)
		return 'TimeSeries({})'.format([i for i in self._timeseries]) 
		'''
		if len(self._timeseries) > 10:
			return "TimeSeries: " + str([(t,v) for (t, v) in zip(self._time[:5], self._value[:5])])\
			+ ".....omitting {} pairs.....".format(len(self._value) - 10) \
			+ str([(t,v) for (t, v) in zip(self._time[-5:], self._value[-5:])])
			'''
			return "TimeSeries" + str([ i for i in self._timeseries[:5]])\
			+ ".....omitting {} pairs.....".format(len(self._value) - 10)\
			+ str([ i  for i in self._timeseries[-5:]])
			'''	
		return 'TimeSeries: ' + str([(t,v) for (t, v) in zip(self._time, self._value)])

	def __str__(self):
		""" Returns a string represenation of the TimeSeries.
		If there are more than 10 elements, the rest are abbreviated.
		"""
		if len(self._timeseries) > 10:
			return "TimeSeries: " + str([(t,v) for (t, v) in zip(self._time[:5], self._value[:5])])\
			+ ".....omitting {} pairs.....".format(len(self._value) - 10) \
			+ str([(t,v) for (t, v) in zip(self._time[-5:], self._value[-5:])])
		return 'TimeSeries: ' + str([(t,v) for (t, v) in zip(self._time, self._value)])



