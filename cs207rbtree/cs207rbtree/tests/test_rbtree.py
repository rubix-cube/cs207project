from cs207rbtree.rbtree import RedBlackNode, RedBlackNodeRef, RedBlackTree, ValueRef, Color
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

def height(tree, rootNode):
    # print("One")
    if rootNode == None:
        return 0
    h = 1 + max(height(tree, tree._follow(rootNode.left_ref)), 
                height(tree, tree._follow(rootNode.right_ref))) 
    print('key=',rootNode.key,' height=',h)
    return h

# def test_balanced(tree, rootNode):
#     if rootNode == None:
#         return True

#     leftNode, rightNode = tree._follow(rootNode.left_ref), tree._follow(rootNode.right_ref)
#     result = abs(height(tree, leftNode) - height(tree, rightNode)) <= 1 and test_balanced(tree, leftNode) and test_balanced(tree, rightNode) 
#     if result == False:
#         print("False key=", rootNode.key)
#     return result
            

def blackproperty(tree, rootNode):
    # http://stackoverflow.com/questions/13848011/how-to-check-the-black-height-of-a-node-for-all-paths-to-its-descendent-leaves
    if rootNode == None:
        return 1

    leftNode  = tree._follow(rootNode.left_ref)
    leftBlackHeight = blackproperty(tree, leftNode)
    if leftBlackHeight == 0:
        return 0

    rightNode = tree._follow(rootNode.right_ref)    
    rightBlackHeight = blackproperty(tree, rightNode)
    if rightBlackHeight == 0:
        return 0

    if leftBlackHeight != rightBlackHeight:
        return 0
    else:
        return leftBlackHeight + 1 if rootNode.color == Color.BLACK else leftBlackHeight

def red_children_are_black(tree, rootNode):
    if rootNode == None:
        return True

    leftNode  = tree._follow(rootNode.left_ref)
    rightNode = tree._follow(rootNode.right_ref)

    if rootNode.color == Color.RED:
        if (leftNode != None and leftNode.color != Color.BLACK) or (rightNode != None and rightNode.color != Color.BLACK):
            return False

    return red_children_are_black(tree, leftNode) and red_children_are_black(tree, rightNode)

def root_black(rootNode):
    return rootNode.color == Color.BLACK

def test_blackproperty():
	t = RedBlackTree(StubStorage())
	t.set(2,1)
	t.set(7,1)
	t.set(3,1)
	t.set(5,1)
	t.set(6,1)
	t.set(1,1)
	t.set(4,1)
	t.set(8,1)
	t.set(9,1)
	t.set(10,1)
	t.set(11,1)
	t.set(12,1)
	t.set(13,1)
	t.set(14,1)
	t.set(15,1)
	t.set(16,1)
	rootNode = t._follow(t._tree_ref)
	assert(blackproperty(t, rootNode) != 0)

def test_root_black_property():
	t = RedBlackTree(StubStorage())
	t.set(2,1)
	t.set(7,1)
	t.set(3,1)
	t.set(5,1)
	t.set(6,1)
	t.set(1,1)
	t.set(4,1)
	t.set(8,1)
	t.set(9,1)
	t.set(10,1)
	t.set(11,1)
	t.set(12,1)
	t.set(13,1)
	t.set(14,1)
	t.set(15,1)
	t.set(16,1)
	rootNode = t._follow(t._tree_ref)
	assert root_black(rootNode)

def test_red_children_are_black():
	t = RedBlackTree(StubStorage())
	t.set(2,1)
	t.set(7,1)
	t.set(3,1)
	t.set(5,1)
	t.set(6,1)
	t.set(1,1)
	t.set(4,1)
	t.set(8,1)
	t.set(9,1)
	t.set(10,1)
	t.set(11,1)
	t.set(12,1)
	t.set(13,1)
	t.set(14,1)
	t.set(15,1)
	t.set(16,1)
	rootNode = t._follow(t._tree_ref)
	assert red_children_are_black(t, rootNode)

def test_red_children_are_black():
	t = RedBlackTree(StubStorage())
	t.set(2,1)
	t.set(7,1)
	t.set(3,1)
	t.set(5,1)
	t.set(6,1)
	t.set(1,1)
	t.set(4,1)
	t.set(8,1)
	t.set(9,1)
	t.set(10,1)
	t.set(11,1)
	t.set(12,1)
	t.set(13,1)
	t.set(14,1)
	t.set(15,1)
	t.set(16,1)
	rootNode = t._follow(t._tree_ref)
	assert red_children_are_black(t, rootNode)



