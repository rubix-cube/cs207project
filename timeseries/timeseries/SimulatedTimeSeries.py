from timeseries.StreamTimeSeriesInterface import StreamTimeSeriesInterface
from itertools import count
from math import sqrt


"""
A helper function for initializing a SimulatedTimeSeries object
For demonstration purpose only
"""
def make_data(start=0, stop=None):
	for _ in count(start):
		if stop and _ > stop:
			break
		yield (_,_) 



class SimulatedTimeSeries(StreamTimeSeriesInterface):

	"""
	SimulatedTimeSeries class, initialized using a generator that produces (time, value) tuples
	In addition to produce() and __iter__, the class also supports iteration over values and times respectively, and calculating online_mean and online_std

	Methods
	-------
	itervalues():
		Generator function that iterates through value component of our time series

	itertimes():
		Generator function that iterates through time component of our time series

	online_mean_generator():
		Generator function that yields (time, mean_value) tuple

	online_std_generator():
		Generator function that yields (time, std_value) tuple

	online_mean():
		Returns a new SimulatedTimeSeries object that is initialized using online_mean_generator
		See Examples for usage

	online_std:
		Returns a new SimulatedTimeSeries object that is initialized using online_std_generator
		Usage the same as online_mean

	NOTE
	----
	SimulatedTimeSeries object should only be initialized using a generator that yields 2-tuple. Using other kinds of generator will result in undefined behaviours

	Examples
	--------
	>>> s = SimulatedTimeSeries(make_data(1,7))
	>>> print(s.produce(7))
	[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)]

	>>> s = SimulatedTimeSeries(make_data(1,7))
	>>> s_mean = s.online_mean() 
	>>> print(s_mean.produce(3))
	[(1, 1), (2, 1.5), (3, 2.0)]

	# Here if we call produce again, s_mean will give us the next 3 mean value based on previous results
	>>> print(s_mean.produce(3))
	[(4, 2.5), (5, 3.0), (6, 3.5)]

	>>> s = SimulatedTimeSeries(make_data(1,7))
	>>> s_mean = s.online_mean()
	>>> print(s_mean.produce(3))
	[(1, 1), (2, 1.5), (3, 2.0)]

	# Here we set s_mean to s.online_mean() again, then the calculation will start from current (time, value) pair
	>>> s_mean = s.online_mean()

	# Notice how the results differ from previous example. The calculation starts from (4, 4)
	>>> s_mean.produce(3)
	[(4, 4), (5, 4.5), (6, 5.0)]

	# The same for online_std

	"""


	"""Takes in a generator containing time series values"""
	def __init__(self, gen):
		self._gen = gen

	""" Takes in an optional chunk specifying the number of tuples to return when iterating
		Returns array of times series tuples
	"""
	def produce(self, chunk=1):
		results = []
		try:
			for i in range(chunk):
				results.append(next(self._gen))
		except:
			pass
		finally:
			return results

	"""Generator function that iterates through TS tuples
	"""
	def __iter__(self):
		for v in self._gen:
			yield v

	"""Generator function iterates through TS values
	"""
	def itervalues(self):
		for v in self._gen:
			yield v[1] # Assumes value is at index 1 in tuple

	"""Generator function iterates through TS times
	"""
	def itertimes(self):
		for v in self._gen:
			yield v[0] # Assumes time is at index 0 in tuple

	"""String representation of Simulated TS
	"""
	def __str__(self):
		return 'SimulatedTimeSeries'

	"""String representation of Simulated TS
	"""
	def __repr__(self):
		return 'SimulatedTimeSeries'


	def online_mean_generator(self):
		k = 1
		it = iter(self)
		while True:
			t, x = next(it)
			if k == 1:
				m = x
			else:
				m = m + (x - m)/k
			yield (t, m)
			k += 1

	def online_std_generator(self):
		k = 1
		it = iter(self)
		while True:
			t, x = next(it)
			if k == 1:
				m = x
				s = 0
			else:
				tmp_m = m + (x - m)/k
				s = s + (x - m) * (x - tmp_m)
				m = tmp_m
			if k == 1:
				yield (t, 0.0)
			else:
				print (t, s, k)
				yield (t, sqrt(s/(k - 1)))
			k += 1

	def online_mean(self):
		return SimulatedTimeSeries(self.online_mean_generator())

	def online_std(self):
		return SimulatedTimeSeries(self.online_std_generator())


if __name__ == "__main__":
	for i in make_data(1,7):
		print(i)
		
	s = SimulatedTimeSeries(make_data(1,7))
	s_std = s.online_std()
	print(s_std.produce(3))
	# s_std = s.online_std()
	print(s_std.produce(3))