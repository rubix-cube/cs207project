import sys, os, inspect
sys.path.insert(0,os.path.split(os.path.split(os.path.realpath(inspect.stack()[0][1]))[0])[0])
import unittest
import binarytree

class BinaryTreeTest(unittest.TestCase):
	'''
	These tests verifies that the main functionalities of the binarytree data strucutre i.e. set, get, get_closer_than are working
	normally.
	''' 
	def test_set_get_before_commit(self):
		'''
		This test verifies that while the database is still connected, we obtained the right values when searching for keys.
		'''
		db = binarytree.connect('test1.dbdb')
		db.set(0, 'a')
		db.set(1, 'b')
		db.set(-1, 'c')
		db.set(-2, 'd')

		self.assertEqual([db.get(0), db.get(-2)], ['a', 'd'])

		db.close()

	def test_empty_if_not_commit(self):
		'''
		This test verifies that the database is empty when reconnected but without any commit made during the previous session.
		'''
		db = binarytree.connect('test2.dbdb')
		db.set(0, 'a')
		db.close()
		db = binarytree.connect('test2.dbdb')
		with self.assertRaises(KeyError):
			db.get(0)

		db.close()

	def test_set_get_after_commit(self):
		'''
		This test verifies that we obtained the right values when searching for keys, when changes where made in a previous session which
		has been commited.
		'''
		db = binarytree.connect('test3.dbdb')
		db.set(0, 'a')
		db.set(1, 'b')
		db.set(-1, 'c')
		db.set(-2, 'd')
		db.commit()
		db.close()

		db = binarytree.connect('test3.dbdb')
		self.assertEqual([db.get(0), db.get(1), db.get(-1), db.get(-2)], ['a', 'b', 'c', 'd'])

		db.close()
	def test_get_closer_before_commit(self):
		'''
		This test verifies that while the database is still connected, we can query keys that are smaller or equal than a particular key.
		'''
		db = binarytree.connect('test4.dbdb')
		db.set(0, 'a')
		db.set(1, 'b')
		db.set(-1, 'c')
		db.set(-2, 'd')

		self.assertEqual(db.get_closer_than(0), [(0, 'a'), (-1, 'c'), (-2, 'd')])

		db.close()

	def test_get_closer_after_commit(self):
		'''
		This test verifies that we can query keys that are smaller or equal than a particular key, when changes where made in a previous session which
		has been commited.
		'''
		db = binarytree.connect('test5.dbdb')
		db.set(0, 'a')
		db.set(1, 'b')
		db.set(-1, 'c')
		db.set(-2, 'd')
		db.commit()
		db.close()

		db = binarytree.connect('test5.dbdb')

		self.assertEqual(db.get_closer_than(0), [(0, 'a'), (-1, 'c'), (-2, 'd')])

		db.close()

	def test_del_key_before_commit_1(self):
		'''
		This test verifies that we can delete a key in the current session.
		'''
		db = binarytree.connect('test6.dbdb')
		db.set(0, 'a')
		db.set(1, 'b')
		db.set(-1, 'c')
		db.set(-2, 'd')

		db.delete(0)
		with self.assertRaises(KeyError):
			db.get(0)

		db.close()

	def test_del_key_before_commit_2(self):
		'''
		This test verifies that we can delete a key in the current sessions without affecting the other (key, value) in the tree.
		'''
		db = binarytree.connect('test7.dbdb')
		db.set(0, 'a')
		db.set(1, 'b')
		db.set(-1, 'c')
		db.set(-2, 'd')

		db.delete(0)
		self.assertEqual([db.get(1), db.get(-1), db.get(-2)], ['b', 'c', 'd'])

		db.close()

	def test_del_key_after_commit_1(self):
		'''
		This test verifies that deletion of keys can be commited and reloaded.
		'''
		db = binarytree.connect('test8.dbdb')
		db.set(0, 'a')
		db.set(1, 'b')
		db.set(-1, 'c')
		db.set(-2, 'd')
		db.delete(0)
		db.commit()
		db.close()

		db = binarytree.connect('test8.dbdb')
		with self.assertRaises(KeyError):
			db.get(0)

		db.close()

	def test_del_key_after_commit_2(self):
		'''
		This test verifies that deletion does not affect key, value pairs and still be commited and reloaded
		'''
		db = binarytree.connect('test9.dbdb')
		db.set(0, 'a')
		db.set(1, 'b')
		db.set(-1, 'c')
		db.set(-2, 'd')
		db.delete(0)
		db.commit()
		db.close()

		db = binarytree.connect('test8.dbdb')
		self.assertEqual([db.get(1), db.get(-1), db.get(-2)], ['b', 'c', 'd'])

		db.close()

	def test_overwrite_value_before_commit(self):
		'''
		This test checks that no duplicate, i.e. a key cannot have two value, can be entered in the tree. 
		'''
		db = binarytree.connect('test10.dbdb')
		db.set(0, 'a')
		db.set(1, 'b')
		db.set(-1, 'c')
		db.set(-2, 'd')

		db.set(-1, 'new')

		self.assertEqual(db.get(-1), 'new')

		db.close()

	def test_overwrite_value_before_commit(self):
		'''
		This test checks that the no duplicate property can be commited
		'''
		db = binarytree.connect('test11.dbdb')
		db.set(0, 'a')
		db.set(1, 'b')
		db.set(-1, 'c')
		db.set(-2, 'd')

		db.set(-1, 'new')

		db.commit()
		db.close()

		db = binarytree.connect('test11.dbdb')

		self.assertEqual(db.get(-1), 'new')

		db.close()


def suite():
	suite = unittest.TestSuite()
	suite.addTest(unittest.makeSuite(BinaryTreeTest))
	return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())