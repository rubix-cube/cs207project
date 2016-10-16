import reprlib, numbers, collections


class TimeSeries:
    """
    Description of time series
        
    Notes
    -----
    PRE: `da_array` is sorted in non-decreasing order (thus items in
        `da_array` must be comparable: implement < and ==)
    POST: 
        - `da_array` is not changed by this function (immutable)
        - returns `index`=-1 if `needle` is not in `da_array`
        - returns an int `index ` in [0:len(da_array)] if
          `index` is in `da_array`
    INVARIANTS:
        - If `needle` in `da_array`, needle in `da_array[rangemin:rangemax]`
          is a loop invariant in the while loop below.
    WARNINGS:
        - If you provide an unsorted array this function is not guaranteed to terminate
        - for multiple copies of a value in the arrar secrched for, the one returned is not guaranteed
        - to be the smallest one.
        
    Examples
    --------
    >>> input = list(range(10))
    >>> binary_search(input, 5)
    5
    """
    

	def __init__(self, input_value, input_time = None):
        """ Constructor for time series
            
            Parameters
            ----------
            input_series : sequence
                a sequence of values in time series 
            input_time : sequence, optional
                a sequence of time intervals for the time series

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
		self._value = list(input_series)
		self._timeseries = zip(self._time, self_value)
		self._dict = dict(zip(self._time), range(0, len(self._time)))


	def __len__(self):
		return len(self._value)

	def __getitem__(self, index):
		if isinstance(index, slice):
			new_slice = slice(self._dict[index.start], self._dict[index.stop], index.step)
			return TimeSeries(self._value, self._time)
		if not isinstance(index, int):
			raise TypeError("Argument index must be either Python slice object or Python int")
		else:
			return self._timeseries[index]

	def __setitem__(self, index, value):
        # if isinstance(index, slice):
        #     print("Slice: ", index)
        #     return cls(self._timeseries[index])
        # elif isinstance(index, numbers.Integral): 
        #     return self._timeseries[index]
        # else:
        #     msg = '{cls.__name__} indices must be integers' 
        #     raise TypeError(msg.format(cls=cls))
        #
		if not isinstance(index, type(self._time[0])):
			raise TypeError("Argument index must have same type as time item")
		else:
			self._value[self._dict[index]] = value
			self._timeseries[self._dict[index]] = (value, index)

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
        for item in self._timeseries:
            yield item

    def itertimes(self):
        pass

