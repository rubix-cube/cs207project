import reprlib, numbers, collections


class TimeSeries:
	"""
	Description of time series class
	
	Attributes
	----------


	Methods
	-------


	Notes
	-----

	"""
	

	def __init__(self, input_value, input_time = None):
		""" Constructor for time series
			
			Parameters
			----------
			input_series : sequence
				a sequence of data
			input_time : sequence, optional
				a sequence of time

			Returns
			-------
			timeseries: TimeSeries
				Description of timeseries object
		"""

		if not isinstance(input_value, collections.Sequence):
			raise TypeError("Argument input_value must be Python sequence ")
		if input_time:
			if not isinstance(input_time, collections.Sequence):
				raise TypeError("Argument input_time must be Python sequence ")
			if len(input_time) != len(input_value):
				raise ValueError("Argument input_value must have same length with input_time")
			self._time = list(input_time)
		else:
			self._time = range(1, len(input_value) + 1)
		self._value = list(input_value)
		self._timeseries = zip(self._time, self_value)
		# self._dict = dict(zip(self._time), range(0, len(self._time)))

	def __len__(self):
		return len(self._value)

	def __getitem__(self, index):
		if isinstance(index, slice):
			# new_slice = slice(self._dict[index.start], self._dict[index.stop], index.step)
			return TimeSeries(self._value[index], self._time[index])
		if not isinstance(index, numbers.Integral):
			raise TypeError("Argument index must be either Python slice object or Python int")
		else:
			return self._timeseries[index]

	def __setitem__(self, index, value):
		if isinstance(index, numbers.Integral): 
		    self._value[index] = value
		else:
		    raise TypeError('Index must be integers')
		#
		# if not isinstance(index, type(self._time[0])):
		# 	raise TypeError("Argument index must have same type as time item")
		# else:
		# 	self._value[self._dict[index]] = value
		# 	self._timeseries[self._dict[index]] = (value, index)

	def __repr__(self):
		#return 'TimeSeries({})'.format([i for i in self._timeseries])
		if len(self._timeseries) > 10:
			return 'TimeSeries(['+', '.join('{}'.format(i) for i in self._timeseries[:5])+\
					'...'+', '.join('{}'.format(i) for i in self._timeseries[-5:])\
					+ ' -- omitting {} objects'.format(len(self._timeseries) - 10)
		return 'TimeSe({})'.format([i for i in self._timeseries]) 	

	def __str__(self):
		""" Returns a string represenation of the TimeSeries.
		If there are more than 100 elements, the rest are abbreviated.
			
			Parameters
			----------
			None

			Returns
			-------
			s : string
				a string representation of the time series
		"""

		if len(self._timeseries) > 10:
			return 'TimeSeries(['+', '.join('{}'.format(i) for i in self._timeseries[:5])+\
					'...'+', '.join('{}'.format(i) for i in self._timeseries[-5:])\
					+ ' -- omitting {} objects'.format(len(self._timeseries) - 10)
		return 'TimeSe({})'.format([i for i in self._timeseries]) 	

	def __iter__(self):
		for v in self._value:
			yield v

	# Peilin: Not sure about this method ???
	def times(self):
		return no.array(self._time)

	def itertimes(self):
		return iter(self._time)

	def __contains__(self, value):
		return value in self._value

	# Peilin: Not sure about this method ???
	def values(self):
		return np.array(self._value)

	def itervalues(self):
		return iter(self._value)

	def items(self):
		return self._timeseries

	def iteritems(self):
		return iter(self._timeseries)


	def __add__(self, otherTS):
		# check otherTS type
		if (not isinstance(otherTS, TimeSeries)) {
			raise TypeError('Can only add with time series')
		}
		# check they have the same length and has equal time domain
		if (len(self) != len(otherTS) or self._time != otherTS._time) {
			raise ValueError(str(self)+' and '+str(otherTS)+' must have the same time points')
		}
		return TimeSeries(self._time, self._value + otherTS._value)

	def __sub__(self, otherTS):
		# check otherTS type
		if (not isinstance(otherTS, TimeSeries)) {
			raise TypeError('Can only subtract with time series')
		}
		# check they have the same length and has equal time domain
		if (len(self) != len(otherTS) or self._time != otherTS._time) {
			raise ValueError(str(self)+' and '+str(otherTS)+' must have the same time points')
		}
		return TimeSeries(self._time, self._value - otherTS._value)


	def __eq__(self, otherTS):
		# check otherTS type
		if (not isinstance(otherTS, TimeSeries)) {
			raise TypeError('Can only eval equal on time series')
		}
		# check they have the same length and has equal time domain
		if (len(self) != len(otherTS) or self._time != otherTS._time) {
			raise ValueError(str(self)+' and '+str(otherTS)+' must have the same time points')
		}
		return self._timeseries == otherTS._timeseries


	def __mul__(self, otherTS):
		# check otherTS type
		if (not isinstance(otherTS, TimeSeries)) {
			raise TypeError('Can only multiply with time series')
		}
		# check they have the same length and has equal time domain
		if (len(self) != len(otherTS) or self._time != otherTS._time) {
			raise ValueError(str(self)+' and '+str(otherTS)+' must have the same time points')
		}
		return TimeSeries(self._time, list(np.array(self._value) * np.array(otherTS._value)))


	def __abs__(self):
		return math.sqrt(sum(x * x for x in self))

	# Peilin: not sure how this should behave ???
	def __bool__(self):
		return bool(abs(self))

	def __neg__(self):
		return TimeSeries(self._time, -v for v in self._value)

	def __pos__(self):
		return TimeSeries(self._time, self._value)
