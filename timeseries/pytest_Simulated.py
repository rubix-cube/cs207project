from pytest import raises
from SimulatedTimeSeries import SimulatedTimeSeries
from SimulatedTimeSeries import make_data


def test_iter():
	ts = SimulatedTimeSeries(make_data(1,3))
	assert list(iter(ts)) == [(0,0),(1,1), (2,2), (3,3)]

def test_produce():
	ts = SimulatedTimeSeries(make_data(1,3))
	assert list(ts.produce(2)) == [(0,0),(1,1)]

def test_produce_more():
	ts = SimulatedTimeSeries(make_data(1,3))
	assert list(ts.produce(2)) == [(0,0), (1,1)]
	assert list(ts.produce(4)) == [(2,2),(3,3)]

def test_iter_val():
	ts = SimulatedTimeSeries(make_data(1,3))
	assert list(ts.itervalues()) == [0,1,2,3]

def test_iter_time():
	ts = SimulatedTimeSeries(make_data(1,3))
	assert list(ts.itertimes()) == [0,1,2,3]


def test_repr_with_time():
	assert repr(SimulatedTimeSeries(make_data(1,3)))=="SimulatedTimeSeries"


def test_str_with_time():
	assert str(SimulatedTimeSeries(make_data(1,3)))=="SimulatedTimeSeries"
