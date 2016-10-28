import abc

class StreamTimeSeriesInterface(abc.ABC):

	@abc.abstractmethod
	def produce(self, chunk=1):
		pass