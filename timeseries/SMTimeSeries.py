from SizedContainerTimeSeriesInterface import SizedContainerTimeSeriesInterface
from FileStorageManager import FileStorageManager
import numpy as np



class SMTimeSeries(SizedContainerTimeSeriesInterface):
	"""
	SMTimeSeries class inherited from SizedContainerTimeSeriesInterface
	
	Attributes
	----------
	_id: int
		unique integer id for each SMtimeseries saved in the storage

	Methods
	-------
	Methods are inherited from SizedContainerTimeSeriesInterface, refer to SizedContainerTimeSeriesInterface for more details

	Property
	--------
	"""
	def __init__(self, time, values, id=None):
		"""
		id is optional and could be None
		auto generate id is handled by FileStorageManager if id is None
		"""
		filesm = FileStorageManager()
		if id==None:
			id = filesm.generateId()
		filesm.store(id, ArrayTImeSeries(input_time, input_value))
		self._id = id
	
	def __len__(self):
		arrayts = FileStorageManager.get(self._id)
		return len(arrayts.values())

	def __getitem__(self, index):
		filesm = FileStorageManager()
		arrayts = filesm.get(self._id)
		return arrayts.getitem(index)
        
	def __setitem__(self, index, value):
		filesm = FileStorageManager()
		arrayts = filesm.get(self._id)
		arrayts.setitem(index, value)
		filesm.store(self._id, arrayts)

	def __iter__(self):
		filesm = FileStorageManager()
		arrayts = filesm.get(self._id)
		iter(arrayts)

	def itertimes(self):
		# raise NotImplementedError('Concrete Implementation are missing for itertimes')
		filesm = FileStorageManager()
		arrayts = filesm.get(self._id)
		return arrayts.itertimes()

	def itervalues(self):
		# raise NotImplementedError('Concrete Implementation are missing for itervalues')
		filesm = FileStorageManager()
		arrayts = filesm.get(self._id)
		return arrayts.itervalues()

	def iteritems(self):
		# raise NotImplementedError('Concrete Implementation are missing for iteritems')
		filesm = FileStorageManager()
		arrayts = filesm.get(self._id)
		return arrayts.iteritems()
		
	def __add__(self, otherTS):
		filesm = FileStorageManager()
		arrayts1 = filesm.get(self._id)
		arrayts2 = filesm.get(otherTS._id)
		arraysum = arrayts1+arrayts2
		return SMTimeSeries(arraysum.times(), arraysum.values())

	def __eq__(self, otherTS):
		filesm = FileStorageManager()
		arrayts1 = filesm.get(self._id)
		arrayts2 = filesm.get(otherTS._id)
		return arrayts1==arrayts2

	def __mul__(self, otherTS):
		filesm = FileStorageManager()
		arrayts1 = filesm.get(self._id)
		arrayts2 = filesm.get(otherTS._id)
		arrayproduct = arrayts1 * arrayts2
		return SMTimeSeries(arrayproduct.times(), arrayproduct.values())

	def __neg__(self):
		filesm = FileStorageManager()
		arrayts = filesm.get(self._id)
		return SMTimeSeries(arrayts.times(), arrayts.values())

	def __pos__(self):
		filesm = FileStorageManager()
		arrayts = filesm.get(self._id)
		return SMTimeSeries(arrayts.times(), arrayts.values())

	def __sub__(self, otherTS):
		filesm = FileStorageManager()
		arrayts1 = filesm.get(self._id)
		arrayts2 = filesm.get(otherTS._id)
		arraydiff = arrayts1 - arrayts2
		return SMTimeSeries(arraydiff.times(), arraydiff.values())

	def interpolate(self, newTimes):
		filesm = FileStorageManager()
		arrayts = filesm.get(self._id)
		arrayinterpolate = arrayts.interpolate(newTimes)
		return SMTimeSeries(arrayinterpolate.times(), arrayinterpolate.values())

	def items(self):
		filesm = FileStorageManager()
		arrayts = filesm.get(self._id)
		return arrayts.items()

	def times(self):
		filesm = FileStorageManager()
		arrayts = filesm.get(self._id)
		return arrayts.times()

	def values(self):
		filesm = FileStorageManager()
		arrayts = filesm.get(self._id)
		return arrayts.values()

	@classmethod
	def from_db(cls, id):
		self._id = id

	def __contains__(self, value):
		filesm = FileStorageManager()
		arrayts = filesm.get(self._id)
		return arrayts.contains(value)

	def __abs__(self):
		filesm = FileStorageManager()
		arrayts = filesm.get(self._id)
		return abs(arrayts)

	def __bool__(self):
		filesm = FileStorageManager()
		arrayts = filesm.get(self._id)
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
		filesm = FileStorageManager()
		arrayts = filesm.get(self._id)
		return repr(arrayts)
		
	def __str__(self):
		""" Returns a string represenation of the TimeSeries.
		If there are more than 10 elements, the rest are abbreviated.
		"""
		filesm = FileStorageManager()
		arrayts = filesm.get(self._id)
		return str(arrayts)


if __name__ == '__main__':
	smts1 = SMTimeSeries(range(5),range(5),1)
	smts2 = SMTimeSeries(range(5),range(5),2)
	print smts1
	print smts1+smts2

