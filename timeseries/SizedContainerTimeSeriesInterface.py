from TimeSeriesInterface import TimeSeriesInterface
from abc import abstractmethod, ABCMeta

class SizedContainerTimeSeriesInterface(TimeSeriesInterface):

	@abstractmethod
	def len(self):
		raise NotImplementedError('Concrete Implementation are missing for len')

	@abstractmethod
	def __getitem__(self, index):
		raise NotImplementedError('Concrete Implementation are missing for __getitem__')

	@abstractmethod
	def __setitem__(self, index, value):
		raise NotImplementedError('Concrete Implementation are missing for __setitem__')

	@abstractmethod
	def __iter__(self):
		raise NotImplementedError('Concrete Implementation are missing for __iter__')

	@abstractmethod
	def itertimes(self):
		raise NotImplementedError('Concrete Implementation are missing for itertimes')

	@abstractmethod
	def itervalues(self):
		raise NotImplementedError('Concrete Implementation are missing for itervalues')

	@abstractmethod
	def iteritems(self):
		raise NotImplementedError('Concrete Implementation are missing for iteritems')

	@abstractmethod
	def __add__(self, otherTS):
		raise NotImplementedError('Concrete Implementation are missing for __add__')

	@abstractmethod
	def __sub__(self, otherTS):
		raise NotImplementedError('Concrete Implementation are missing for __sub__')

	@abstractmethod
	def __eq__(self, otherTS):
		raise NotImplementedError('Concrete Implementation are missing for __eq__')

	@abstractmethod
	def __mul__(self, otherTS):
		raise NotImplementedError('Concrete Implementation are missing for __mul__')

	@abstractmethod
	def __neg__(self):
		raise NotImplementedError('Concrete Implementation are missing for __neg__')

	@abstractmethod
	def __pos__(self):
		raise NotImplementedError('Concrete Implementation are missing for __pos__')



