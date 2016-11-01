from StreamTimeSeriesInterface import StreamTimeSeriesInterface
from itertools import count


def make_data(m, stop=None):
	for _ in count():
		if stop and _ > stop:
			break
		yield (_,_) 

class SimulatedTimeSeries(StreamTimeSeriesInterface):

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

	"""Iterator function that iterates through TS tuples
	"""
	def __iter__(self):
		for v in self._gen:
			yield v

	"""Iterator function iterates through TS values
	"""
	def itervalues(self):
		for v in self._gen:
			yield v[1] # Assumes value is at index 0 in tuple

	"""Iterator function iterates through TS times
	"""
	def itertimes(self):
		for v in self._gen:
			yield v[0] # Assumes time is at index 1 in tuple

	"""String representation of Simulated TS
	"""
	def __str__(self):
		return 'SimulatedTimeSeries'

	"""String representation of Simulated TS
	"""
	def __repr__(self):
		return 'SimulatedTimeSeries'


if __name__ == "__main__":
	s = SimulatedTimeSeries(make_data(1,7))
	print(s)
	print(s.produce(3))
	print(s.produce(3))