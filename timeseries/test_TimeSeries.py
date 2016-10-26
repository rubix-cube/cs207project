# from pytest import raises
from TimeSeries import TimeSeries
import unittest
import random
from numpy.linalg import norm
import numpy as np

'''
def test_valid_ts_no_time():
	self.ts = TimeSeries([9,3])
	assert self.ts.value == [9,3]
	assert self.ts.time == [1,2]

def test_valid_ts_with_time():
	self.ts = TimeSeries([9,3],[3,5])
	assert self.ts.value == [9,3]
	assert self.ts.time == [3,5]

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
'''
class MyTest(unittest.TestCase):

	def setUp(self):
		self.ts = TimeSeries([1,2,3],[0.1,0.2,0.3])
		self.ts2 = TimeSeries([1,2,3],[0.1,0.2,0.5])
		self.ts3 = TimeSeries([1,2,5],[0.1,0.2,0.3])
		self.ts4 = TimeSeries(range(1, 12), range(1, 12))
		
		self.val1 = random.sample(range(100), 20)
		self.val2 = random.sample(range(100), 20)
		self.time = [random.random() for i in range(20)]

		self.ts5 = TimeSeries(self.val1, self.time)
		self.ts6 = TimeSeries(self.val2, self.time)


	def test_init(self):
		self.assertEqual(self.ts._value, [1,2,3])
		self.assertEqual(self.ts._time, [0.1,0.2,0.3])
		self.assertEqual(list(self.ts._timeseries), [(0.1,1),(0.2,2),(0.3,3)])

	def test_equal(self):
		self.assertTrue(self.ts == self.ts)
		self.assertFalse(self.ts == self.ts3)
		with self.assertRaises(ValueError):
			self.ts == self.ts2
		

	def test_getitem(self):
		# self.ts = TimeSeries([1,2,3],[0.1,0.2,0.3])
		self.assertEqual(self.ts[0], 1)
		self.assertEqual(self.ts[1], 2)
		self.assertEqual(self.ts[2], 3)
		self.assertTrue(self.ts[0:2] == TimeSeries([1,2], [0.1,0.2]))

	def test_setitem(self):
		self.ts[0] = 0.5
		self.ts[1] = 0.6
		self.ts[2] = 0.7
		self.assertTrue(self.ts == TimeSeries([0.5,0.6,0.7], [0.1,0.2,0.3]))
		

	def test_print(self):
		self.assertEqual(str(self.ts), 'TimeSeries: [(0.1, 1), (0.2, 2), (0.3, 3)]')
		self.ts[0] = 0.5
		self.ts[1] = 0.6
		self.ts[2] = 0.7
		self.assertEqual(str(self.ts), 'TimeSeries: [(0.1, 0.5), (0.2, 0.6), (0.3, 0.7)]')

		self.assertEqual(str(self.ts4), 'TimeSeries: [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)].....omitting 1 pairs.....[(7, 7), (8, 8), (9, 9), (10, 10), (11, 11)]')

		self.assertEqual(repr(self.ts4), 'TimeSeries: [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)].....omitting 1 pairs.....[(7, 7), (8, 8), (9, 9), (10, 10), (11, 11)]')

	def test_iters(self):
		self.assertEqual(list(self.ts.itertimes()), [0.1,0.2,0.3])
		self.assertEqual(list(self.ts.itervalues()), [1,2,3])
		self.assertEqual(list(self.ts.iteritems()), [(0.1,1),(0.2,2),(0.3,3)])

	def test_add_mul_sub(self):
		ts = self.ts5 + self.ts6
		self.assertEqual(ts._value, list(np.array(self.val1) + np.array(self.val2)))
		self.assertEqual(ts._time, self.ts5._time)

		ts = self.ts5 - self.ts6
		self.assertTrue(ts._value, list(np.array(self.val1) - np.array(self.val2)))
		self.assertEqual(ts._time, self.ts5._time)

		ts = self.ts5 * self.ts6
		self.assertTrue(ts._value, list(np.array(self.val1) * np.array(self.val2)))
		self.assertEqual(ts._time, self.ts5._time)

	def test_abs(self):
		self.assertEqual(abs(self.ts5), norm(self.ts5._value))

	def test_neg_pos(self):
		ts = -self.ts5
		self.assertEqual(ts._value, list(-1 * np.array(self.ts5._value)))
		self.assertEqual(ts._time, self.ts5._time)

		ts = +self.ts5
		self.assertEqual(ts._value,self.ts5._value)
		self.assertEqual(ts._time, self.ts5._time)





