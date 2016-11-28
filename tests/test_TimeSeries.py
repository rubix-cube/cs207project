from pytest import raises
from timeseries.TimeSeries import TimeSeries
import numpy as np
import math
from timeseries.TimeSeries import check_length

#Test constructor
def test_valid_ts_no_time():
	ts = TimeSeries([9,3])
	assert ts._value == [9,3]
	assert list(ts._time) == [1,2]
	assert ts._timeseries == [(1,9),(2,3)]

def test_valid_ts_with_time():
	ts = TimeSeries([9,3],[3,5])
	assert ts._value == [9,3]
	assert ts._time == [3,5]
	assert ts._timeseries == [(3,9),(5,3)]

def test_valid_ts_range_no_time():
	ts = TimeSeries(range(0,5))
	assert ts._value == [0,1,2,3,4]
	assert list(ts._time) == [1,2,3,4,5]
	assert ts._timeseries == [(1,0),(2,1),(3,2),(4,3),(5,4)]

def test_valid_ts_range_time():
	ts = TimeSeries(range(0,5),range(2,7))
	assert ts._value == [0,1,2,3,4]
	assert ts._time == [2,3,4,5,6]
	assert ts._timeseries == [(2,0),(3,1),(4,2),(5,3),(6,4)]

def test_empty_ts():
	ts = TimeSeries([])
	assert ts._value == []
	assert list(ts._time) == []
	assert ts._timeseries == []

def test_not_seq_no_time():
	with raises(TypeError):
		TimeSeries(3)

def test_not_seq_val():
	with raises(TypeError):
		TimeSeries(3, [1])

def test_not_seq_time():
	with raises(TypeError):
		TimeSeries([3], 1)
    
def test_length_not_match_time():
	with raises(ValueError):
		TimeSeries([3,9], [1])
        
def test_length_not_match_val():
	with raises(ValueError):
		TimeSeries([3], [1,2])

#Test length function
def test_length_no_time():
	assert len(TimeSeries([1,4,3])) == 3

def test_length_time():
	assert len(TimeSeries([1,4,3],[2,3,5])) == 3

def test_length_empty():
	assert len(TimeSeries([])) == 0

#Test getitem
def test_get_with_time():
	ts = TimeSeries([9,3],[3,5])
	assert ts[1] == (5,3)

def test_get_no_time():
	ts = TimeSeries([9,3])
	assert ts[1] == (2,3)

def test_get_out_of_range_no_time():
	ts = TimeSeries([9,3])
	with raises(IndexError):
		ts[3]

def test_get_out_of_range_time():
	ts = TimeSeries([9,3],[3,5])
	with raises(IndexError):
		ts[3]

#Test getitem with slice object
def test_get_slice_time():
	ts = TimeSeries([9,3,12],[3,5,7])
	assert ts[1:3:1] == TimeSeries([3,12],[5,7])

def test_get_slice_no_time():
	ts = TimeSeries([9,3,12])
	assert ts[1:3:1] == TimeSeries([3,12],[2,3])

def test_get_out_of_range_slice_no_time():
	ts = TimeSeries([9,3])
	assert ts[2:4:1] == TimeSeries([],[])

def test_get_out_of_range_slice_time():
	ts = TimeSeries([9,3],[3,5])
	assert ts[2:4:1] == TimeSeries([],[])

#Test setitem
def test_set_with_time():
	ts = TimeSeries([9,3],[3,5])
	ts[1] = 8
	assert ts[1] == (5,8)

def test_set_no_time():
	ts = TimeSeries([9,3])
	ts[1] = 10
	assert ts[1] == (2,10)

def test_set_not_int_char():
	ts = TimeSeries([9,3])
	with raises(TypeError):
		ts['a'] = 10

def test_set_not_int_list():
	ts = TimeSeries([9,3])
	with raises(TypeError):
		ts[[1,2]] = 10

def test_set_out_of_range_no_time():
	ts = TimeSeries([9,3])
	with raises(IndexError):
		ts[3] = 10

def test_set_out_of_range_with_time():
	ts = TimeSeries([9,3],[4,8])
	with raises(IndexError):
		ts[3] = 10

def test_set_out_of_range_empty():
	ts = TimeSeries([])
	with raises(IndexError):
		ts[1] = 10

#Test __repr__
def test_repr_no_time():
	assert repr(TimeSeries([1,3,5]))=="TimeSeries: [(1, 1), (2, 3), (3, 5)]"

def test_repr_with_time():
	assert repr(TimeSeries([1,3,5], [5,7,9]))=="TimeSeries: [(5, 1), (7, 3), (9, 5)]"

def test_repr_no_time_long():
	assert repr(TimeSeries(range(1,30,2)))=="TimeSeries: [(1, 1), (2, 3), (3, 5), (4, 7), (5, 9)].....omitting 5 pairs.....[(11, 21), (12, 23), (13, 25), (14, 27), (15, 29)]"

def test_repr_with_time_long():
	assert repr(TimeSeries(range(1,30,2),range(5,34,2)))=="TimeSeries: [(5, 1), (7, 3), (9, 5), (11, 7), (13, 9)].....omitting 5 pairs.....[(25, 21), (27, 23), (29, 25), (31, 27), (33, 29)]"

#Test __str__
def test_str_no_time():
	assert str(TimeSeries([1,3,5]))=="TimeSeries: [(1, 1), (2, 3), (3, 5)]"

def test_str_with_time():
	assert str(TimeSeries([1,3,5], [5,7,9]))=="TimeSeries: [(5, 1), (7, 3), (9, 5)]"

def test_str_no_time_long():
	assert str(TimeSeries(range(1,30,2)))=="TimeSeries: [(1, 1), (2, 3), (3, 5), (4, 7), (5, 9)].....omitting 5 pairs.....[(11, 21), (12, 23), (13, 25), (14, 27), (15, 29)]"

def test_str_with_time_long():
	assert str(TimeSeries(range(1,30,2),range(5,34,2)))=="TimeSeries: [(5, 1), (7, 3), (9, 5), (11, 7), (13, 9)].....omitting 5 pairs.....[(25, 21), (27, 23), (29, 25), (31, 27), (33, 29)]"

#Test iters
def test_iter():
	ts = TimeSeries(range(0,7))
	assert list(iter(ts)) == [0,1,2,3,4,5,6]

def test_iter_val():
	ts = TimeSeries(range(0,7))
	assert list(ts.itervalues()) == [0,1,2,3,4,5,6]

def test_iter_time():
	ts = TimeSeries(range(0,7))
	assert list(ts.itertimes()) == [1,2,3,4,5,6,7]

def test_iter_pair():
	ts = TimeSeries(range(0,7))
	assert list(ts.iteritems()) == [(1,0),(2,1),(3,2),(4,3),(5,4),(6,5),(7,6)]

def test_val():
	ts = TimeSeries(range(0,7))
	assert np.array_equal(ts.values(), np.array([0,1,2,3,4,5,6]))

def test_time():
	ts = TimeSeries(range(0,7))
	assert np.array_equal(ts.times(), np.array([1,2,3,4,5,6,7]))

def test_pair():
	ts = TimeSeries(range(0,7))
	assert ts.items() == [(1,0),(2,1),(3,2),(4,3),(5,4),(6,5),(7,6)]

#Test operations
#__eq__
def test_equal():
	ts1 = TimeSeries(range(0,7))
	ts2 = TimeSeries([0,1,2,3,4,5,6])
	assert ts1 == ts2

def test_not_equal_len():
	ts1 = TimeSeries(range(0,7))
	ts2 = TimeSeries(range(0,6))
	with raises(ValueError):
		ts1 == ts2

def test_not_equal_time():
	ts1 = TimeSeries(range(0,7))
	ts2 = TimeSeries(range(0,7), range(2,9))
	with raises(ValueError):
		ts1 == ts2

def test_not_equal_val():
	ts1 = TimeSeries(range(0,7))
	ts2 = TimeSeries(range(2,9))
	assert ts1 != ts2


#__add__
def test_add_valid():
	ts1 = TimeSeries(range(0,7))
	ts2 = TimeSeries(range(3,10))
	assert (ts1+ts2) == TimeSeries([3,5,7,9,11,13,15])

def test_add_time_not_match_len():
	ts1 = TimeSeries(range(0,6))
	ts2 = TimeSeries(range(3,10))
	with raises(ValueError):
		ts1+ts2

def test_add_time_not_match_time():
	ts1 = TimeSeries(range(0,6), range(2,8))
	ts2 = TimeSeries(range(3,10))
	with raises(ValueError):
		ts1+ts2

def test_add_wrong_type():
	ts1 = TimeSeries(range(0,6))
	with raises(TypeError):
		ts1+4	

def test_add_const():
	ts = TimeSeries([1,2,3])
	assert ts.addConst(5) == TimeSeries([6,7,8])

def test_sub_const():
	ts = TimeSeries([1,2,3])
	assert ts.subConst(4) == TimeSeries([-3,-2,-1])

def test_mult_const():
	ts = TimeSeries([1,2,3])
	assert ts.multConst(5) == TimeSeries([5,10,15])

def test_sub_valid():
	ts1 = TimeSeries(range(0,7))
	ts2 = TimeSeries(range(3,10))
	assert (ts2-ts1) == TimeSeries([3,3,3,3,3,3,3])

def test_sub_time_not_match_len():
	ts1 = TimeSeries(range(0,6))
	ts2 = TimeSeries(range(3,10))
	with raises(ValueError):
		ts1-ts2

def test_sub_time_not_match_time():
	ts1 = TimeSeries(range(0,6), range(2,8))
	ts2 = TimeSeries(range(3,10))
	with raises(ValueError):
		ts1-ts2

def test_sub_wrong_type():
	ts1 = TimeSeries(range(0,6))
	with raises(TypeError):
		ts1-4	

def test_mult_valid():
	ts1 = TimeSeries(range(0,7))
	ts2 = TimeSeries(range(3,10))
	assert (ts2*ts1) == TimeSeries([0,4,10,18,28,40,54])

def test_mult_time_not_match_len():
	ts1 = TimeSeries(range(0,6))
	ts2 = TimeSeries(range(3,10))
	with raises(ValueError):
		ts1*ts2

def test_mult_time_not_match_time():
	ts1 = TimeSeries(range(0,6), range(2,8))
	ts2 = TimeSeries(range(3,10))
	with raises(ValueError):
		ts1*ts2

def test_mult_wrong_type():
	ts1 = TimeSeries(range(0,6))
	with raises(TypeError):
		ts1*4


#Test contains
def test_contains_true():
	ts  = TimeSeries(range(0,6))
	assert (5 in ts) == True

def test_contains_false():
	ts = TimeSeries(range(0,6))
	assert (6 in ts) == False


def test_abs_all_pos():
	ts = TimeSeries([2,3,4])
	assert abs(ts) == math.sqrt(29)

def test_abs_all_neg():
	ts = TimeSeries([-2,-3,-4])
	assert abs(ts) == math.sqrt(29)

def test_bool_true():
	ts = TimeSeries([-2,-3,-4])
	assert bool(ts)==True

def test_bool_false():
	ts = TimeSeries([])
	assert bool(ts)==False

def test_neg_all_pos():
	ts = TimeSeries([2,3,4])
	assert -ts == TimeSeries([-2,-3,-4])

def test_neg_all_neg():
	ts = TimeSeries([-2,-3,-4])
	assert -ts == TimeSeries([2,3,4])

def test_neg_mix():
	ts = TimeSeries([-2,3,-4])
	assert -ts == TimeSeries([2,-3,4])

def test_pos_all_pos():
	ts = TimeSeries([2,3,4])
	assert +ts == TimeSeries([2,3,4])

def test_pos_all_neg():
	ts = TimeSeries([-2,-3,-4])
	assert +ts == TimeSeries([-2,-3,-4])

def test_pos_mix():
	ts = TimeSeries([-2,3,-4])
	assert +ts == TimeSeries([-2,3,-4])

#Test interpolation
def test_interpolate_mid():
	ts = TimeSeries([1,2,3],[0,5,10])
	assert ts.interpolate([1]) == TimeSeries([1.2],[1])

def test_interpolate_same():
	ts = TimeSeries([1,2,3],[0,5,10])
	assert ts.interpolate([5]) == TimeSeries([2],[5])

def test_interpolate_small():
	ts = TimeSeries([1,2,3],[0,5,10])
	assert ts.interpolate([-5]) == TimeSeries([1],[-5])

def test_interpolate_big():
	ts = TimeSeries([1,2,3],[0,5,10])
	assert ts.interpolate([15]) == TimeSeries([3],[15])

def test_interpolate_list():
	ts = TimeSeries([1,2,3],[0,5,10])
	assert ts.interpolate([7.5,15]) == TimeSeries([2.5,3],[7.5,15])

def test_lazy_eval():
	thunk = check_length(TimeSeries(range(0,4),range(1,5)), TimeSeries(range(1,5),range(2,6)))
	assert thunk.eval()==True

# test stats
def test_mean():
	ts = TimeSeries([1,2,3])
	assert ts.mean() == np.mean([1,2,3])

def test_std():
	ts = TimeSeries([1,2,3])
	assert ts.std() == np.std([1,2,3])



