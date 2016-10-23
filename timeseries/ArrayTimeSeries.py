import numpy as np
class ArrayTimeSeries(TimeSeries):
	def __init__(self, seq):
		if not isinstance(input_value, collections.Sequence):
			raise TypeError("Argument input_value must be Python sequence ")
		if input_time:
			if not isinstance(input_time, collections.Sequence):
				raise TypeError("Argument input_time must be Python sequence ")
			if len(input_time) != len(input_value):
				raise ValueError("Argument input_value must have same length with input_time")
			self._time = np.array(input_time)
		else:
			self._time = np.arange(1, len(input_value) + 1)
		self._value = np.array(input_value)
		self._timeseries = np.array(zip(self._time, self_value))
		self._dict = dict(zip(self._time), range(0, len(self._time)))

