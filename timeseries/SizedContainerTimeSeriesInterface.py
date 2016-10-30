from TimeSeriesInterface import TimeSeriesInterface
from abc import abstractmethod, ABCMeta
import numpy as numpy
import math

class SizedContainerTimeSeriesInterface(TimeSeriesInterface):

	@abstractmethod
	def __len__(self):
		raise NotImplementedError('Concrete Implementation are missing for __len__')

	@abstractmethod
	def __getitem__(self, index):
		raise NotImplementedError('Concrete Implementation are missing for __getitem__')

	@abstractmethod
	def __setitem__(self, index, value):
		raise NotImplementedError('Concrete Implementation are missing for __setitem__')

	@abstractmethod
	def __iter__(self):
		raise NotImplementedError('Concrete Implementation are missing for __iter__')

	@abstractmethod
	def itertimes(self):
		raise NotImplementedError('Concrete Implementation are missing for itertimes')

	@abstractmethod
	def itervalues(self):
		raise NotImplementedError('Concrete Implementation are missing for itervalues')

	@abstractmethod
	def iteritems(self):
		raise NotImplementedError('Concrete Implementation are missing for iteritems')

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

	def __abs__(self):
		return math.sqrt(sum(x * x for x in self))

	def __bool__(self):
		return bool(abs(self))

	def __repr__(self):
		#return 'TimeSeries({})'.format([i for i in self._timeseries])
		"""
		if len(self._timeseries) > 10:
			return 'TimeSeries(['+','.join('{}'.format(i) for i in self._timeseries[:5])\
					+ '...'+','.join('{}'.format(i) for i in self._timeseries[-5:]) + '])'\
					+ ' -- omitting {} objects'.format(len(self._timeseries) - 10)
		return 'TimeSeries({})'.format([i for i in self._timeseries]) 
		"""
		if len(self._timeseries) > 10:
			return "TimeSeries: " + str([(t,v) for (t, v) in zip(self._time[:5], self._value[:5])])\
			+ ".....omitting {} pairs.....".format(len(self._value) - 10) \
			+ str([(t,v) for (t, v) in zip(self._time[-5:], self._value[-5:])])
			'''
			return "TimeSeries" + str([ i for i in self._timeseries[:5]])\
			+ ".....omitting {} pairs.....".format(len(self._value) - 10) \
			+ str([ i  for i in self._timeseries[-5:]])
			'''	
		return 'TimeSeries: ' + str([(t,v) for (t, v) in zip(self._time, self._value)])

	def __str__(self):
		""" Returns a string represenation of the TimeSeries.
		If there are more than 100 elements, the rest are abbreviated.
			
			Parameters
			----------
			None

			Returns
			-------
			s : string
				a string representation of the time series
		"""
		if len(self._timeseries) > 10:
			return "TimeSeries: " + str([(t,v) for (t, v) in zip(self._time[:5], self._value[:5])])\
			+ ".....omitting {} pairs.....".format(len(self._value) - 10) \
			+ str([(t,v) for (t, v) in zip(self._time[-5:], self._value[-5:])])
		return 'TimeSeries: ' + str([(t,v) for (t, v) in zip(self._time, self._value)])



