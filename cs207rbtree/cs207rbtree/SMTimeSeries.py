from SizedContainerTimeSeriesInterface import SizedContainerTimeSeriesInterface
from FileStorageManager import FileStorageManager
import numpy as np


class SMTimeSeries(SizedContainerTimeSeriesInterface):
	"""
	SMTimeSeries class inherited from SizedContainerTimeSeriesInterface
	
	Attributes
	----------
	_time: list of numerics
		time component of our time series

	Methods
	-------
	Methods are inherited from SizedContainerTimeSeriesInterface, refer to SizedContainerTimeSeriesInterface for more details

	Property
	--------
	"""

	self._storage = FileStorageManager()

	def __init__(self, time, values, id=None):
		timeseries = np.vstack((time, values)).T.astype(np.float64) # Pair time with value
		

	@classmethod
	def from_db(cls, id):
		self._storage.get(id)