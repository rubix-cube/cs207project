import reprlib

class TimeSeries:

	def __init__(self, input_series):
		self._timeseries = input_series

	def __len__(self):
		return len(self._timeseries)

	def __getitem__(self, index):
		if isinstance(index, slice):
			return TimeSeries(self._timeseries[index])
		return self._timeseries[index]

	def __setitem__(self, index, value):
		self._timeseries[index] = value

	def __repr__(self):
		return 'TimeS({})'.format([i for i in self._timeseries])

	def __str__(self):
		if len(self._timeseries) > 100:
			return 'TimeSeries(['+', '.join('{}'.format(i) for i in self._timeseries[:10])+'...'+', '.join('{}'.format(i) for i in self._timeseries[-10:])\
					+ ' -- omitting {} objects'.format(len(self._timeseries) - 20)
		return 'TimeSe({})'.format([i for i in self._timeseries]) 	

	def __iter__(self):
		for item in self._timeseries:
			yield item

	def itertimes(self):
		pass

