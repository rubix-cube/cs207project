from pytest import raises
from timeseries.SimulatedTimeSeries import SimulatedTimeSeries
from timeseries.SimulatedTimeSeries import make_data


def test_iter():
	ts = SimulatedTimeSeries(make_data(0,3))
	assert list(iter(ts)) == [(0,0),(1,1), (2,2), (3,3)]

def test_produce():
	ts = SimulatedTimeSeries(make_data(0,3))
	assert list(ts.produce(2)) == [(0,0),(1,1)]

def test_produce_more():
	ts = SimulatedTimeSeries(make_data(0,3))
	assert list(ts.produce(2)) == [(0,0), (1,1)]
	assert list(ts.produce(4)) == [(2,2),(3,3)]

def test_iter_val():
	ts = SimulatedTimeSeries(make_data(0,3))
	assert list(ts.itervalues()) == [0,1,2,3]

def test_iter_time():
	ts = SimulatedTimeSeries(make_data(0,3))
	assert list(ts.itertimes()) == [0,1,2,3]


def test_repr_with_time():
	assert repr(SimulatedTimeSeries(make_data(0,3)))=="SimulatedTimeSeries"


def test_str_with_time():
	assert str(SimulatedTimeSeries(make_data(0,3)))=="SimulatedTimeSeries"


def test_online_mean():
	s = SimulatedTimeSeries(make_data(1,6))
	s_mean = s.online_mean()
	assert s_mean.produce(3) == [(1, 1.0), (2, 1.5), (3, 2.0)]
	assert s_mean.produce(3) == [(4, 2.5), (5, 3.0), (6, 3.5)]

	s = SimulatedTimeSeries(make_data(1,6))
	s_mean = s.online_mean()
	s_mean.produce(3)
	s_mean = s.online_mean()
	assert s_mean.produce(3) == [(4, 4.0), (5, 4.5), (6, 5.0)]

def test_online_std():
	s = SimulatedTimeSeries(make_data(1,6))
	s_std = s.online_std()
	assert s_std.produce(3) == [(1, 0.0), (2, 0.7071067811865476), (3, 1.0)]
	assert s_std.produce(3) == [(4, 1.2909944487358056), (5, 1.5811388300841898), (6, 1.8708286933869707)]

	s = SimulatedTimeSeries(make_data(1,6))
	s_std = s.online_std()
	s_std.produce(3)
	s_std = s.online_std()
	assert s_std.produce(3) == [(4, 0.0), (5, 0.7071067811865476), (6, 1.0)]



