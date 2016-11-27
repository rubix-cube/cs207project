from cs207rbtree.cs207rbtree.rbtree import RedBlackNode, RedBlackNodeRef, RedBlackTree, ValueRef
from pytest import raises
import pickle
import random

class StubStorage(object):
	def __init__(self):
		self.d = [0]
		self.locked = False

	def lock(self):
		if not self.locked:
			self.locked = True
			return True
		else:
			return False

	def unlock(self):
		pass

	def get_root_address(self):
		return 0

	def write(self, string):
		address = len(self.d)
		self.d.append(string)
		return address

	def read(self, address):
		return self.d[address]


def test_missing_key():
	tree = RedBlackTree(StubStorage())
	with raises(KeyError):
		tree.get('key')

def test_set_and_get_key():
	tree = RedBlackTree(StubStorage())
	tree.set('a', 'b')
	assert tree.get('a') == 'b'

def test_random_set_and_get_keys():
	tree = RedBlackTree(StubStorage())
	ten_k = list(range(10000))
	pairs = list(zip(random.sample(ten_k, 10), random.sample(ten_k, 10)))
	for i, (k, v) in enumerate(pairs, start=1):
		tree.set(k, v)
	for k, v in pairs:
		assert tree.get(k) == v

def test_overwrite_and_get_key():
	tree = RedBlackTree(StubStorage())
	tree.set('a', 'b')
	tree.set('a', 'c')
	assert tree.get('a') == 'c'

def test_to_bytes_leaf():
	n = RedBlackNode(RedBlackNodeRef(), 'k', ValueRef(address=999), RedBlackNodeRef(), 0)
	pickled = RedBlackNodeRef.referent_to_bytes(n)
	d = pickle.loads(pickled)
	assert d['left'] == 0
	assert d['key'] == 'k'
	assert d['value'] == 999
	assert d['right'] == 0
	assert d['color'] == 0

def test_to_bytes_nonleaf():
	left_ref = RedBlackNodeRef(address=123)
	right_ref = RedBlackNodeRef(address=321)
	n = RedBlackNode(left_ref, 'k', ValueRef(address=999), right_ref, 1)
	pickled = RedBlackNodeRef.referent_to_bytes(n)
	d = pickle.loads(pickled)
	assert d['left'] == 123
	assert d['key'] == 'k'
	assert d['value'] == 999
	assert d['right'] == 321
	assert d['color'] == 1



