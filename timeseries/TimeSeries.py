import reprlib, numbers

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
    
    def __init__(self, input_series):

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
        self._timeseries = input_series

    def __len__(self):
        return len(self._timeseries)

    def __getitem__(self, index):

        if isinstance(index, slice):
            print("Slice: ", index)
            return TimeSeries(self._timeseries[index])
        return self._timeseries[index]

    def __getitem__(self, index):
        cls = type(self)

        if isinstance(index, slice):
            print("Slice: ", index)
            return cls(self._timeseries[index])
        elif isinstance(index, numbers.Integral): 
            return self._timeseries[index]
        else:
            msg = '{cls.__name__} indices must be integers' 
            raise TypeError(msg.format(cls=cls))

    def __setitem__(self, index, value):
        self._timeseries[index] = value

    def __repr__(self):
        return 'TimeSeries({})'.format([i for i in self._timeseries])

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

        if len(self._timeseries) > 100:
            return 'TimeSeries(['+', '.join('{}'.format(i) for i in self._timeseries[:10])+'...'+', '.join('{}'.format(i) for i in self._timeseries[-10:])\
                    + ' -- omitting {} objects'.format(len(self._timeseries) - 20)
        return 'TimeSeries({})'.format([i for i in self._timeseries])   

    def __iter__(self):
        for item in self._timeseries:
            yield item

    def itertimes(self):
        pass

