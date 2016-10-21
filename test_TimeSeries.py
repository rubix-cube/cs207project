from pytest import raises
import TimeSeries

def test_valid_ts_no_time():
	ts = TimeSeries([9,3])
	assert ts.value == [9,3]
	assert ts.time == [1,2]

def test_valid_ts_with_time():
	ts = TimeSeries([9,3],[3,5])
	assert ts.value == [9,3]
	assert ts.time == [3,5]

def test_not_seq_no_time():
	with raises(TypeError):
		TimeSeries(3)

def test_not_seq_no_time():
	with raises(TypeError):
		TimeSeries(3, [1])
    
def test_length_not_match_time():
	with raises(ValueError):
		TimeSeries([3,9], [1])
        
def test_length_not_match_val():
    with raises(ValueError):
		TimeSeries([3], [1,2])