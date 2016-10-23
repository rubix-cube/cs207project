from pytest import raises
from TimeSeries import TimeSeries

#Test constructor
def test_valid_ts_no_time():
	ts = TimeSeries([9,3])
	assert ts._value == [9,3]
	assert ts._time == [1,2]

def test_valid_ts_with_time():
	ts = TimeSeries([9,3],[3,5])
	assert ts._value == [9,3]
	assert ts._time == [3,5]

def test_not_seq_no_time():
	with raises(TypeError):
		TimeSeries(3)

def test_not_seq_with_time():
	with raises(TypeError):
		TimeSeries(3, [1])

def test_length_not_match_time():
	with raises(ValueError):
		TimeSeries([3,9], [1])

def test_length_not_match_val():
	with raises(ValueError):
		TimeSeries([3], [1,2])

#Test length function
def test_length():
	assert len(TimeSeries([1,4,3])) == 3

#Test getitem
def test_get_with_time():
	ts = TimeSeries([9,3],[3,5])
	assert ts[3] == (3,9)

def test_get_no_time():
	ts = TimeSeries([9,3])
	assert ts[2] == (2,3)

def test_get_out_of_range_no_time():
	ts = TimeSeries([9,3])
	with raises(TypeError):
		ts[3]

'''
def test_get_out_of_range_with_time():
	ts = TimeSeries([9,3],[4,8])
	with raises(TypeError):
		ts[5]
'''


#Test setitem
def test_set_with_time():
	ts = TimeSeries([9,3],[3,5])
	ts[3] = 8
	assert ts[3] == (3,8)

def test_set_no_time():
	ts = TimeSeries([9,3])
	ts[2] = 10
	assert ts[2] == (2,10)

def test_set_out_of_range_no_time():
	ts = TimeSeries([9,3])
	with raises(TypeError):
		ts[3] = 10

'''
def test_set_out_of_range_with_time():
	ts = TimeSeries([9,3],[4,8])
	with raises(TypeError):
		ts[5] = 10
'''


#Test __repr__
def test_repr_with_time():
	assert repr(TimeSeries([1,3,5])=="[(1,1), (2,3), (3,5)]")

def test_repr_no_time():
	assert repr(TimeSeries([1,3,5], [5,7,9])=="[(5,1), (7,3), (9,5)]")


#Test __str__
def test_str_with_time():
	assert str(TimeSeries([1,3,5])=="[(1,1), (2,3), (3,5)]")

def test_str_no_time():
	assert str(TimeSeries([1,3,5], [5,7,9])=="[(5,1), (7,3), (9,5)]")


