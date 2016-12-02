# cs207project
We implemented 3 time series interfaces along with 3 kinds of time series classes.

For our *cs207rbtree* module, see documentation [here](https://github.com/rubix-cube/cs207project/tree/master/cs207rbtree)

Team 9 implements similarity search for us which can be found [here](https://github.com/rubix-cube/cs207project/tree/master/simsearch)

## Interfaces

### TimeSeriesInterface
This is the ABC for all subclasses we implemented. It contains 3 abstract methods which are `__iter__`, `__str__`, and `__repr__`. We put `__iter__` here because we want all time series subclasses to support at least one kind of iterations.

### SizedContainerTimeSeriesInterface
Inherited from TimeSeriesInterface, this interface is the base class for TimeSeries class and ArrayTimeSeries class. It has a large amount of methods, both abstract and non-abstract, that we consider important for a sized container-typed time series class. We want its subcalsses to support common sequence operations such as `__getitem__`, `__setitem__`, `__len__` etc, and also some element-wise arithmetic operations such as addition, substraction and multiplication.

## Classes

### TimeSeries Class
Inherited from SizedContainerTimeSeriesInterface, this class implements most methods in its base class. It uses lists as its underlying storage. See class documentation for more details.

### ArrayTimeSeries Class
Almost the same as TimeSeries class, except that it uses numpy array rather than list as its underlying storage.

### SimulatedTimeSeries Class
Inherited from StreamTimeSeriesInterface, this class has no underlying storage. Rather, it takes into a generator and produces time series data on demand.

The class supports online mean and standard deviation calculation. See class documentation and examples for more details.

[![Build Status](https://travis-ci.org/rubix-cube/cs207project.svg?branch=master)](https://travis-ci.org/rubix-cube/cs207project)

[![Coverage Status](https://coveralls.io/repos/github/Peilin-D/cs207project/badge.svg?branch=master)](https://coveralls.io/github/Peilin-D/cs207project?branch=master)
