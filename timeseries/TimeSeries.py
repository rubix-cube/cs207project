import reprlib, numbers, collections


class TimeSeries:
    """
    Description of time series
        
    Notes
    -----
    PRE: 
        - The values within input_value are of the same type and are numbers.
        - Input time is a series of numbers representaing time. The values are
          of the same type and should be numbers.
    POST: 
        - `da_array` is not changed by this function (immutable)
    WARNINGS:
        - If you provide an unsorted array this function is not guaranteed to terminate
        
        
    Examples
    --------
    >>> ts = TimeSeries(range(1,1000))
    >>> ts[1]
    1
    """
    

	def __init__(self, input_value, input_time = None):
        """ Constructor for time series
            
            Parameters
            ----------
            input_series : sequence
                a sequence of values in time series 
            input_time : sequence, optional
                a sequence of time intervals for the time series
                if no input time is given, a default evenly spaced time interval
                will be used
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
			self._time = list(range(1, len(input_value) + 1))
		self._value = list(input_value)
		self._timeseries = zip(self._time, self._value)
		self._dict = dict(zip(self._time, range(0, len(self._time))))


	def __len__(self):
		return len(self._value)

	def __getitem__(self, index):
        """ Get item for time series
            
            Parameters
            ----------
            index : time
                The time(s) in time series for which value is needed.
                A range can be specified using slice notation [x:y:z] where
                x,y,z are valid times.

            Returns
            -------
            value : the value in time series corresponding to given time input
        """
		if isinstance(index, slice):
			new_slice = slice(self._dict[index.start], self._dict[index.stop], index.step)
			return TimeSeries(self._value, self._time)
		if not isinstance(index, int):
			raise TypeError("Argument index must be either Python slice object or Python int")
		else:
			return self._timeseries[index]

	def __setitem__(self, index, value):
		if not isinstance(index, type(self._time[0])):
			raise TypeError("Argument index must have same type as time item")
		else:
			self._value[self._dict[index]] = value
			self._timeseries[self._dict[index]] = (value, index)

	def interpolate(newTimes):
		"""returns a new TimeSeries objects with times given and newly computed values 
			The times passed in should be in ascending order and be numbers.

			Parameters
			----------
			None

			Returns
			-------
		"""
	    newValues = []
	    time, value = self._time, self._value
	    counter, n = 1, len(time)
	    for t in newTimes:
	        while counter < n:
	            if t < time[0]:
	                newValues.append(value[0])
	                break
	            elif t > time[n-1]:
	                newValues.append(value[n-1])
	                break
	            elif time[counter-1] <= t <= time[counter]:
	                newVal = t + t * ((value[counter]-value[counter-1]) / (time[counter] - time[counter-1]))
	                newValues.append(newVal)
	                counter += 1
	                break
	    return TimeSeries(newValues, newTimes)

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

