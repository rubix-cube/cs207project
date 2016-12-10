## TimeSeries Package
We implemented 4 time series interfaces along with 5 kinds of time series classes.

* Install: `$ python setup.py install`
* Test: `$ python setup.py test`
* Documentation: `$ python setup.py docs`

## Interfaces

### TimeSeriesInterface
This is the ABC for all subclasses we implemented. It contains 3 abstract methods which are `__iter__`, `__str__`, and `__repr__`. We put `__iter__` here because we want all time series subclasses to support at least one kind of iterations.

### SizedContainerTimeSeriesInterface
Inherited from TimeSeriesInterface, this interface is the base class for TimeSeries class and ArrayTimeSeries class. It has a large amount of methods, both abstract and non-abstract, that we consider important for a sized container-typed time series class. We want its subcalsses to support common sequence operations such as `__getitem__`, `__setitem__`, `__len__` etc, and also some element-wise arithmetic operations such as addition, substraction and multiplication.

### StreamTimeSeriesInterface
Inherited from TimeseriesInterface, this interface is the base class for SimulatedTimeSeries class. It has no underlying storage for our time series, and the subclasses should suppport a produce method that produce certain size of data on demand.

### StorageManagerInterface
This is the base class for FileStorageManager class. It has only 3 abstract method as described below:
1. store(id:int/string, t:SizedContainerTimeSeriesInterface)->SizedContainerTimeSeriesInterface
2. size(id:int/string)->int
3. get(id:int/string)->SizedContainerTimeSeriesInterface
This interface is tend to store the timeseries data persistently on disk so that we will not lose our data even when the serve is down.

## Classes

### TimeSeries Class
Inherited from SizedContainerTimeSeriesInterface, this class implements most methods in its base class. It uses lists as its underlying storage. See class documentation for more details.

### ArrayTimeSeries Class
Almost the same as TimeSeries class, except that it uses numpy array rather than list as its underlying storage.

### SimulatedTimeSeries Class
Inherited from StreamTimeSeriesInterface, this class has no underlying storage. Rather, it takes into a generator and produces time series data on demand.

The class supports online mean and standard deviation calculation. See class documentation and examples for more details.

### SMTimeSeries Class
Inherited from SizedContainerTimeSeriesInterface, this class has no on memory storage. Instead, the class store the timeseries values on disk via a storage manager class.

The class support all member method of SizedContainerTimeSeriesInterface, like add, multiple, len etc. It will also automatically save the result of t1 + t2 onto disk.

### FileStorageManager Class
Inherited from StorageManagerInterface and implemented 3 major method, store, get, size. It could store any timeseries as a 2D numpy array on the disk persistently with given id as key. It could also return SMTimeseries instance for query with key. The key and file relation is also kept on disk. So even when the server goes down, we will not lose our timeseries data nor the key-file relation.
