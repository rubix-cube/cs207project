from TimeSeriesInterface import TimeSeriesInterface
import abc

class StreamTimeSeriesInterface(TimeSeriesInterface):

	@abc.abstractmethod
	def produce(self, chunk=1):
		pass