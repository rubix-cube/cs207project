import os
import os.path
import tempfile
from pytest import raises
from cs207rbtree.cs207rbtree import *

def test_new_database_file():
	temp_dir = tempfile.mkdtemp()
	new_tempfile_name = os.path.join(temp_dir, 'new.db')
	db = connect(new_tempfile_name)
	db.set('a', 'aye')
	db.commit()
	db.close()

def test_persistence():
	temp_dir = tempfile.mkdtemp()
	tempfile_name = os.path.join(temp_dir, 'existing.db')
	db = connect(tempfile_name)
	db.set('b', 'bee')
	db.set('a', 'aye')
	db.set('c', 'see')
	db.commit()
	db.set('d', 'dee')
	db.close()
	db = connect(tempfile_name)
	assert db.get('a') == 'aye'
	assert db.get('b') == 'bee'
	assert db.get('c') == 'see'
	with raises(KeyError):
		db.get('d')
	db.close()

