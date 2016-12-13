import pytest
from pytest import raises
import numpy as np
import math

from timeseries.SMTimeSeries import SMTimeSeries, StorageManager
# from timeseries.FileStorageManager import FileStorageManager

def clean_up():
	StorageManager.clean_up()

@pytest.fixture(scope='session', autouse=True)
def finalize(request):
	request.addfinalizer(clean_up)

#Test constructor
def test_construct_with_id_num():
	ts = SMTimeSeries([3,5], [9,3], 1990)
	arrayts = StorageManager.get(ts._id)
	assert ts._id == str(1990)
	assert np.array_equal(arrayts._value,np.array([9,3]))
	assert np.array_equal(arrayts._time,np.array([3,5]))
	assert np.array_equal(arrayts._timeseries, np.array([(3,9),(5,3)]))

def test_construct_with_id_str():
	ts = SMTimeSeries([3,5], [9,3], 'givenid')
	arrayts = StorageManager.get(ts._id)
	assert ts._id == 'givenid'
	assert np.array_equal(arrayts._value,np.array([9,3]))
	assert np.array_equal(arrayts._time,np.array([3,5]))
	assert np.array_equal(arrayts._timeseries, np.array([(3,9),(5,3)]))

def test_valid_ts_with_time():
	ts = SMTimeSeries([3,5], [9,3])
	arrayts = StorageManager.get(ts._id)
	assert np.array_equal(arrayts._value,np.array([9,3]))
	assert np.array_equal(arrayts._time,np.array([3,5]))
	assert np.array_equal(arrayts._timeseries, np.array([(3,9),(5,3)]))

def test_valid_ts_range_time():
	ts = SMTimeSeries(range(2,7),range(0,5))
	arrayts = StorageManager.get(ts._id)
	assert np.array_equal(arrayts._value,np.array([0,1,2,3,4]))
	assert np.array_equal(arrayts._time,np.array([2,3,4,5,6]))
	assert np.array_equal(arrayts._timeseries,np.array([(2,0),(3,1),(4,2),(5,3),(6,4)]))

def test_empty_ts():
	ts = SMTimeSeries([],[])
	arrayts = StorageManager.get(ts._id)
	for t in arrayts._value == np.array([]):
		assert t
	for t in arrayts._time == np.array([]):
		assert t
	for t in arrayts._timeseries == np.array([]):
		assert t	

def test_not_seq_time():
	with raises(TypeError):
		SMTimeSeries(3, [1])

def test_not_seq_val():
	with raises(TypeError):
		SMTimeSeries([3], 1)
    
def test_length_not_match_time():
	with raises(ValueError):
		SMTimeSeries([3,9], [1])
        
def test_length_not_match_val():
	with raises(ValueError):
		SMTimeSeries([3], [1,2])

#Test length function

def test_length_time():
	assert len(SMTimeSeries([1,4,3],[2,3,5])) == 3

def test_length_empty():
	assert len(SMTimeSeries([],[])) == 0

#Test getitem
def test_get_with_time():
	ts = SMTimeSeries([3,5], [9,3])
	for t in ts[1] == [5,3]:
		assert t

def test_get_out_of_range_time():
	ts = SMTimeSeries([3,5],[9,3])
	with raises(IndexError):
		ts[3]

#Test getitem with slice object
def test_get_slice_time():
	ts = SMTimeSeries([3,5,7], [9,3,12])
	tsslice = ts[1:3:1]
	assert  SMTimeSeries(tsslice.times(), tsslice.values())== SMTimeSeries([5,7],[3,12])

def test_get_out_of_range_slice_time():
	ts = SMTimeSeries([3,5], [9,3])
	tsslice = ts[1:3:1]
	assert  SMTimeSeries(tsslice.times(), tsslice.values()) == SMTimeSeries([5],[3])

#Test setitem
def test_set_with_time():
	ts = SMTimeSeries([3,5],[9,3])
	ts[1] = 8
	for t in ts[1] == [5,8]:
		assert t

def test_set_not_int_char():
	ts = SMTimeSeries([3,5],[9,3])
	with raises(TypeError):
		ts['a'] = 10

def test_set_not_int_list():
	ts = SMTimeSeries([3,5],[9,3])
	with raises(TypeError):
		ts[[1,2]] = 10

def test_set_out_of_range_with_time():
	ts = SMTimeSeries([3,5],[9,3])
	with raises(IndexError):
		ts[3] = 10

def test_set_out_of_range_empty():
	ts = SMTimeSeries([],[])
	with raises(IndexError):
		ts[1] = 10

#Test __repr__

def test_repr_with_time():
	assert repr(SMTimeSeries([5,7,9], [1,3,5]))=="TimeSeries: [(5.0, 1.0), (7.0, 3.0), (9.0, 5.0)]"

def test_repr_with_time_long():
	assert repr(SMTimeSeries(range(5,34,2),range(1,30,2)))=="TimeSeries: [(5.0, 1.0), (7.0, 3.0), (9.0, 5.0), (11.0, 7.0), (13.0, 9.0)].....omitting 5 pairs.....[(25.0, 21.0), (27.0, 23.0), (29.0, 25.0), (31.0, 27.0), (33.0, 29.0)]"

#Test __str__
def test_str_with_time():
	assert str(SMTimeSeries([5,7,9], [1,3,5]))=="TimeSeries: [(5.0, 1.0), (7.0, 3.0), (9.0, 5.0)]"

def test_str_with_time_long():
	assert str(SMTimeSeries(range(5,34,2), range(1,30,2)))=="TimeSeries: [(5.0, 1.0), (7.0, 3.0), (9.0, 5.0), (11.0, 7.0), (13.0, 9.0)].....omitting 5 pairs.....[(25.0, 21.0), (27.0, 23.0), (29.0, 25.0), (31.0, 27.0), (33.0, 29.0)]"

#Test iters
def test_iter():
	ts = SMTimeSeries(range(1,8),range(0,7))
	assert list(iter(ts)) == [0,1,2,3,4,5,6]

def test_iter_val():
	ts = SMTimeSeries(range(1,8),range(0,7))
	assert list(ts.itervalues()) == [0,1,2,3,4,5,6]

def test_iter_time():
	ts = SMTimeSeries(range(1,8),range(0,7))
	assert list(ts.itertimes()) == [1,2,3,4,5,6,7]

def test_iter_pair():
	ts = SMTimeSeries(range(1,8),range(0,7))
	assert np.array_equal(np.array(list(ts.iteritems())), np.array([(1,0),(2,1),(3,2),(4,3),(5,4),(6,5),(7,6)]))

def test_val():
	ts = SMTimeSeries(range(1,8),range(0,7))
	assert np.array_equal(ts.values(), np.array([0,1,2,3,4,5,6]))

def test_time():
	ts = SMTimeSeries(range(1,8),range(0,7))
	assert np.array_equal(ts.times(), np.array([1,2,3,4,5,6,7]))

def test_pair():
	ts = SMTimeSeries(range(1,8),range(0,7))
	assert np.array_equal(ts.items(), np.array([(1,0),(2,1),(3,2),(4,3),(5,4),(6,5),(7,6)]))

#Test operations
#__eq__
def test_equal():
	ts1 = SMTimeSeries(range(1,8),range(0,7))
	ts2 = SMTimeSeries(range(1,8),[0,1,2,3,4,5,6])
	assert ts1 == ts2

def test_not_equal_len():
	ts1 = SMTimeSeries(range(1,8),range(0,7))
	ts2 = SMTimeSeries(range(1,7),range(0,6))
	with raises(ValueError):
		ts1 == ts2

def test_not_equal_time():
	ts1 = SMTimeSeries(range(1,8),range(0,7))
	ts2 = SMTimeSeries(range(2,9),range(0,7))
	with raises(ValueError):
		ts1 == ts2

def test_not_equal_val():
	ts1 = SMTimeSeries(range(1,8),range(0,7))
	ts2 = SMTimeSeries(range(1,8),range(2,9))
	assert ts1 != ts2


#__add__
def test_add_valid():
	ts1 = SMTimeSeries(range(1,8),range(0,7))
	ts2 = SMTimeSeries(range(1,8),range(3,10))
	assert (ts1+ts2) == SMTimeSeries(range(1,8),[3,5,7,9,11,13,15])

def test_add_time_not_match_len():
	ts1 = SMTimeSeries(range(1,7),range(0,6))
	ts2 = SMTimeSeries(range(1,8),range(3,10))
	with raises(ValueError):
		ts1+ts2

def test_add_time_not_match_time():
	ts1 = SMTimeSeries(range(0,6), range(2,8))
	ts2 = SMTimeSeries(range(1,7), range(3,9))
	with raises(ValueError):
		ts1+ts2

def test_add_wrong_type():
	ts1 = SMTimeSeries(range(1,7),range(0,6))
	with raises(AttributeError):
		ts1+4	

def test_sub_valid():
	ts1 = SMTimeSeries(range(1,8),range(0,7))
	ts2 = SMTimeSeries(range(1,8),range(3,10))
	assert (ts2-ts1) == SMTimeSeries(range(1,8),[3,3,3,3,3,3,3])

def test_sub_time_not_match_len():
	ts1 = SMTimeSeries(range(1,7),range(0,6))
	ts2 = SMTimeSeries(range(1,8),range(3,10))
	with raises(ValueError):
		ts1-ts2

def test_sub_time_not_match_time():
	ts1 = SMTimeSeries(range(0,6), range(2,8))
	ts2 = SMTimeSeries(range(1,7), range(3,9))
	with raises(ValueError):
		ts1-ts2

def test_sub_wrong_type():
	ts1 = SMTimeSeries(range(1,7),range(0,6))
	with raises(AttributeError):
		ts1-4	

def test_mult_valid():
	ts1 = SMTimeSeries(range(1,8),range(0,7))
	ts2 = SMTimeSeries(range(1,8),range(3,10))
	assert (ts2*ts1) == SMTimeSeries(range(1,8),[0,4,10,18,28,40,54])

def test_mult_time_not_match_len():
	ts1 = SMTimeSeries(range(1,7),range(0,6))
	ts2 = SMTimeSeries(range(1,8),range(3,10))
	with raises(ValueError):
		ts1*ts2

def test_mult_time_not_match_time():
	ts1 = SMTimeSeries(range(0,6), range(2,8))
	ts2 = SMTimeSeries(range(1,7), range(3,9))
	with raises(ValueError):
		ts1*ts2

def test_mult_wrong_type():
	ts1 = SMTimeSeries(range(1,7),range(0,6))
	with raises(AttributeError):
		ts1*4

def test_add_const():
	ts = SMTimeSeries([0,1,2], [3,4,5])
	assert ts.addConst(5) == SMTimeSeries([0,1,2], [8,9,10])

def test_sub_const():
	ts = SMTimeSeries([0,1,2], [3,4,5])
	assert ts.subConst(5) == SMTimeSeries([0,1,2], [-2,-1,0])
def test_mult_const():
	ts = SMTimeSeries([0,1,2], [3,4,5])
	assert ts.multConst(5) == SMTimeSeries([0,1,2], [15,20,25])


#Test contains
def test_contains_true():
	ts = SMTimeSeries(range(1,7),range(0,6))
	assert (5 in ts) == True

def test_contains_false():
	ts = SMTimeSeries(range(1,7),range(0,6))
	assert (6 in ts) == False


def test_abs_all_pos():
	ts = SMTimeSeries([1,2,3], [2,3,4])
	assert abs(ts) == math.sqrt(29)

def test_abs_all_neg():
	ts = SMTimeSeries([1,2,3], [-2,-3,-4])
	assert abs(ts) == math.sqrt(29)

def test_bool_true():
	ts = SMTimeSeries([1,2,3], [-2,-3,-4])
	assert bool(ts)==True

def test_bool_false():
	ts = SMTimeSeries([],[])
	assert bool(ts)==False

def test_neg_all_pos():
	ts = SMTimeSeries([1,2,3], [2,3,4])
	assert -ts == SMTimeSeries([1,2,3], [-2,-3,-4])

def test_neg_all_neg():
	ts = SMTimeSeries([1,2,3], [-2,-3,-4])
	assert -ts == SMTimeSeries([1,2,3], [2,3,4])

def test_neg_mix():
	ts = SMTimeSeries([1,2,3], [-2,3,-4])
	assert -ts == SMTimeSeries([1,2,3], [2,-3,4])

def test_pos_all_pos():
	ts = SMTimeSeries([1,2,3], [2,3,4])
	assert +ts == SMTimeSeries([1,2,3], [2,3,4])

def test_pos_all_neg():
	ts = SMTimeSeries([1,2,3], [-2,-3,-4])
	assert +ts == SMTimeSeries([1,2,3], [-2,-3,-4])

def test_pos_mix():
	ts = SMTimeSeries([1,2,3], [-2,3,-4])
	assert +ts == SMTimeSeries([1,2,3], [-2,3,-4])

#Test interpolation
def test_interpolate_mid():
	ts = SMTimeSeries([0,5,10], [1,2,3])
	assert ts.interpolate([7.5]) == SMTimeSeries([7.5], [2.5])

def test_interpolate_same():
	ts = SMTimeSeries([0,5,10], [1,2,3])
	assert ts.interpolate([10]) == SMTimeSeries([10], [3])

def test_interpolate_small():
	ts = SMTimeSeries([0,5,10], [1,2,3])
	assert ts.interpolate([-5]) == SMTimeSeries([-5], [1])

def test_interpolate_big():
	ts = SMTimeSeries([0,5,10], [1,2,3])
	assert ts.interpolate([15]) == SMTimeSeries([15], [3])

def test_interpolate_list():
	ts = SMTimeSeries([0,5,10], [1,2,3])
	assert ts.interpolate([7.5,15]) == SMTimeSeries([7.5,15], [2.5,3])
'''
# test stats
def test_mean():
	ts = SMTimeSeries([0,1,2], [3,4,5])
	arrayts = StorageManager.get(ts._id)
	assert ts.mean() == np.mean([3,4,5])

def test_std():
	ts = SMTimeSeries([0,1,2], [3,4,5])
	assert ts.std() == np.std([3,4,5])
'''
