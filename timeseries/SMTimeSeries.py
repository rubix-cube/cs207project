from SizedContainerTimeSeriesInterface import SizedContainerTimeSeriesInterface
from FileStorageManager import StorageManager
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
	def __init__(self, time, values, id=None):
		timeseries = np.vstack((time, values)).T.astype(np.float64) # Pair time with value
		StorageManager.store(id, timeseries)
		
	def __add__(self):
		pass

	def __eq__(self):
		pass

	def __getitem__(self):
		pass
	def __mul__(self):
		pass
	def __neg__(self):
		pass
	def __pos__(self):
		pass
	def __setitem__(self):
		pass
	def __sub__(self):
		pass
	def interpolate(self):
		pass
	def items(self):
		pass 
	def times(self):
		pass
	def values(self):
		pass

	@classmethod
	def from_db(cls, id):
		print ("Needed to be implemented")

SMTimeSeries(range(5),range(5),1)
SMTimeSeries(range(5),range(5),2)
print (StorageManager._id)