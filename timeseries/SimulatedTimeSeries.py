from StreamTimeSeriesInterface import StreamTimeSeriesInterface
from itertools import count


def make_data(m, stop=None):
    for _ in count():
        if stop and _ > stop:
            break
        yield 1.0e09 

class SimulatedTimeSeries(StreamTimeSeriesInterface):

	def __init__(self, gen):
		self._gen = gen

	def produce(self, chunk=1):
		results = []
		try:
			for i in range(chunk):
				results.append(next(self._gen))
		except:
			pass
		finally:
			return results


if __name__ == "__main__":
	s = SimulatedTimeSeries(make_data(1,7))
# 	print(s.produce(3))
# 	print(s.produce(3))
# 	print(s.produce(3))