import os
import tempfile

from cs207rbtree.physical import Storage

def _get_superblock_and_data(value):
	superblock = value[:Storage.SUPERBLOCK_SIZE]
	data = value[Storage.SUPERBLOCK_SIZE:]
	return superblock,data

def _get_f_contents(f):
	f.flush()
	with open(f.name, 'rb') as File:
		return File.read()

def test_init_ensures_superblock():
	f = tempfile.NamedTemporaryFile()
	p = Storage(f)
	EMPTY_SUPERBLOCK = (b'\x00' * Storage.SUPERBLOCK_SIZE)
	f.seek(0, os.SEEK_END)
	value = _get_f_contents(f)
	assert value == EMPTY_SUPERBLOCK

def test_write():
	f = tempfile.NamedTemporaryFile()
	p = Storage(f)
	p.write(b'ABCDE')
	value = _get_f_contents(f)
	superblock, data = _get_superblock_and_data(value)
	assert data == b'\x00\x00\x00\x00\x00\x00\x00\x05ABCDE'

def test_read():
	f = tempfile.NamedTemporaryFile()
	p = Storage(f)
	f.seek(Storage.SUPERBLOCK_SIZE)
	f.write(b'\x00\x00\x00\x00\x00\x00\x00\x0801234567')
	value = p.read(Storage.SUPERBLOCK_SIZE)
	assert value == b'01234567'

def test_commit_root_address():
	f = tempfile.NamedTemporaryFile()
	p = Storage(f)
	p.commit_root_address(257)
	root_bytes = _get_f_contents(f)[:8]
	assert root_bytes == b'\x00\x00\x00\x00\x00\x00\x01\x01'

def test_get_root_address():
	f = tempfile.NamedTemporaryFile()
	p = Storage(f)
	f.seek(0)
	f.write(b'\x00\x00\x00\x00\x00\x00\x02\x02')
	root_address = p.get_root_address()
	assert root_address == 514

def test_workflow():
	f = tempfile.NamedTemporaryFile()
	p = Storage(f)
	a1 = p.write(b'one')
	a2 = p.write(b'two')
	p.commit_root_address(a2)
	a3 = p.write(b'three')
	assert p.get_root_address() == a2
	a4 = p.write(b'four')
	p.commit_root_address(a4)
	assert p.read(a1) == b'one'
	assert p.read(a2) == b'two'
	assert p.read(a3) == b'three'
	assert p.read(a4) == b'four'
	assert p.get_root_address() == a4
