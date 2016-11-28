from timeseries.TimeSeriesInterface import TimeSeriesInterface
import abc

class StreamTimeSeriesInterface(TimeSeriesInterface):
	"""
	Interface for stream time series
	No underlying storage for our time series, and the subclasses should suppport a produce method that produce 'chunk' size of data on demand

	Methods
	-------
	produce(chunk):
		Takes in an optional chunk specifying the number of tuples to return when iterating
		Returns array of times series tuples

	"""
	@abc.abstractmethod
	def produce(self, chunk=1):
		raise NotImplementedError('Concrete Implementation are missing for produce()')
