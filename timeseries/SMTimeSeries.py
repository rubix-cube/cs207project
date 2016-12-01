from timeseries.SizedContainerTimeSeriesInterface import SizedContainerTimeSeriesInterface
from timeseries.FileStorageManager import StorageManager
from timeseries.ArrayTimeSeries import ArrayTimeSeries
import numpy as np


class SMTimeSeries(SizedContainerTimeSeriesInterface):
	"""
	SMTimeSeries class inherited from SizedContainerTimeSeriesInterface
	
	Attributes
	----------
	_id: int
		unique integer id for each SMtimeseries saved on disk

	Methods
	-------
	Methods are inherited from SizedContainerTimeSeriesInterface, refer to SizedContainerTimeSeriesInterface for more details

	Property
	--------
	"""
	def __init__(self, input_time, input_value, id=None):
		"""
		id is optional and could be None
		auto generate id is handled by FileStorageManager if id is None
		"""
		if id==None:
			id = StorageManager.generateId()
		StorageManager.store(str(id), ArrayTimeSeries(input_time, input_value))
		self._id = str(id)
	
	def __len__(self):
		arrayts = StorageManager.get(self._id)
		return len(arrayts.values())

	def __getitem__(self, index):
		arrayts = StorageManager.get(self._id)
		return arrayts[index]
        
	def __setitem__(self, index, value):
		arrayts = StorageManager.get(self._id)
		arrayts[index] = value
		StorageManager.store(self._id, arrayts)

	def __iter__(self):
		arrayts = StorageManager.get(self._id)
		return iter(arrayts)

	def itertimes(self):
		# raise NotImplementedError('Concrete Implementation are missing for itertimes')
		arrayts = StorageManager.get(self._id)
		return arrayts.itertimes()

	def itervalues(self):
		# raise NotImplementedError('Concrete Implementation are missing for itervalues')
		arrayts = StorageManager.get(self._id)
		return arrayts.itervalues()

	def iteritems(self):
		# raise NotImplementedError('Concrete Implementation are missing for iteritems')
		arrayts = StorageManager.get(self._id)
		return arrayts.iteritems()
		
	def __add__(self, otherTS):
		arrayts1 = StorageManager.get(self._id)
		arrayts2 = StorageManager.get(otherTS._id)
		arraysum = arrayts1+arrayts2
		return SMTimeSeries(arraysum.times(), arraysum.values())

	def addConst(self, num):
		arrayts1 = StorageManager.get(self._id)
		arraysum = arrayts1.addConst(num)
		return SMTimeSeries(arraysum.times(), arraysum.values())

	def subConst(self, num):
		arrayts1 = StorageManager.get(self._id)
		arraydiff = arrayts1.subConst(num)
		return SMTimeSeries(arraydiff.times(), arraydiff.values())

	def multConst(self, num):
		arrayts1 = StorageManager.get(self._id)
		arrayproduct = arrayts1.multConst(num)
		return SMTimeSeries(arrayproduct.times(), arrayproduct.values())

	def __eq__(self, otherTS):
		arrayts1 = StorageManager.get(self._id)
		arrayts2 = StorageManager.get(otherTS._id)
		return arrayts1==arrayts2

	def __mul__(self, otherTS):
		arrayts1 = StorageManager.get(self._id)
		arrayts2 = StorageManager.get(otherTS._id)
		arrayproduct = arrayts1 * arrayts2
		return SMTimeSeries(arrayproduct.times(), arrayproduct.values())

	def __neg__(self):
		arrayts = StorageManager.get(self._id)
		return SMTimeSeries(arrayts.times(), -arrayts.values())

	def __pos__(self):
		arrayts = StorageManager.get(self._id)
		return SMTimeSeries(arrayts.times(), arrayts.values())

	def __sub__(self, otherTS):
		arrayts1 = StorageManager.get(self._id)
		arrayts2 = StorageManager.get(otherTS._id)
		arraydiff = arrayts1 - arrayts2
		return SMTimeSeries(arraydiff.times(), arraydiff.values())

	def interpolate(self, newTimes):
		arrayts = StorageManager.get(self._id)
		arrayinterpolate = arrayts.interpolate(newTimes)
		return SMTimeSeries(arrayinterpolate.times(), arrayinterpolate.values())

	def items(self):
		arrayts = StorageManager.get(self._id)
		return arrayts.items()

	def times(self):
		arrayts = StorageManager.get(self._id)
		return arrayts.times()

	def values(self):
		arrayts = StorageManager.get(self._id)
		return arrayts.values()

	@classmethod
	def from_db(cls, id):
		self._id = id

	def __contains__(self, value):
		arrayts = StorageManager.get(self._id)
		return (value in arrayts)

	def __abs__(self):
		arrayts = StorageManager.get(self._id)
		return abs(arrayts)

	def __bool__(self):
		arrayts = StorageManager.get(self._id)
		return bool(abs(arrayts))


	def __repr__(self):
		#return 'TimeSeries({})'.format([i for i in self._timeseries])
		'''
		if len(self._timeseries) > 10:
			return 'TimeSeries(['+','.join('{}'.format(i) for i in self._timeseries[:5])\
					+ '...'+','.join('{}'.format(i) for i in self._timeseries[-5:]) + '])'\
					+ ' -- omitting {} objects'.format(len(self._timeseries) - 10)
		return 'TimeSeries({})'.format([i for i in self._timeseries]) 
		'''
		arrayts = StorageManager.get(self._id)
		return repr(arrayts)
		
	def __str__(self):
		""" Returns a string represenation of the TimeSeries.
		If there are more than 10 elements, the rest are abbreviated.
		"""
		arrayts = StorageManager.get(self._id)
		return str(arrayts)

'''
if __name__ == '__main__':
	smts1 = SMTimeSeries(range(5),range(5),1)
	smts2 = SMTimeSeries(range(5),range(5),2)
	print (smts1)
	print smts1+smts2
'''
