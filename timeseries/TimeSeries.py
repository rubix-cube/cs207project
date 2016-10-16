import reprlib
import collections

class TimeSeries:

	def __init__(self, input_value, input_time = None):
		if not isinstance(input_value, collections.Sequence):
			raise TypeError("Argument input_value must be Python sequence ")
		if input_time:
			if not isinstance(input_time, collections.Sequence):
				raise TypeError("Argument input_time must be Python sequence ")
			if len(input_time) != len(input_value):
				raise ValueError("Argument input_value must have same length with input_time")
			self._time = list(input_time)
		else:
			self._time = range(1, len(input_value) + 1)
		self._value = list(input_series)
		self._timeseries = zip(self._time, self_value)
		self._dict = dict(zip(self._time), range(0, len(self._time)))


	def __len__(self):
		return len(self._value)

	def __getitem__(self, index):
		if isinstance(index, slice):
			new_slice = slice(self._dict[index.start], self._dict[index.stop], index.step)
			return TimeSeries(self._value, self._time)
		if not isinstance(index, int):
			raise TypeError("Argument index must be either Python slice object or Python int")
		else:
			return self._timeseries[index]

	def __setitem__(self, index, value):
		if not isinstance(index, type(self._time[0])):
			raise TypeError("Argument index must have same type as time item")
		else:
			self._value[self._dict[index]] = value
			self._timeseries[self._dict[index]] = (value, index)

	def __repr__(self):
		#return 'TimeSeries({})'.format([i for i in self._timeseries])
		if len(self._timeseries) > 10:
			return 'TimeSeries(['+', '.join('{}'.format(i) for i in self._timeseries[:5])+\
				'...'+', '.join('{}'.format(i) for i in self._timeseries[-5:])\
					+ ' -- omitting {} objects'.format(len(self._timeseries) - 10)
		return 'TimeSe({})'.format([i for i in self._timeseries]) 	

	def __str__(self):
		if len(self._timeseries) > 10:
			return 'TimeSeries(['+', '.join('{}'.format(i) for i in self._timeseries[:5])+\
				'...'+', '.join('{}'.format(i) for i in self._timeseries[-5:])\
					+ ' -- omitting {} objects'.format(len(self._timeseries) - 10)
		return 'TimeSe({})'.format([i for i in self._timeseries]) 	

	def __iter__(self):
		for item in self._timeseries:
			yield item

	def itertimes(self):
		pass

