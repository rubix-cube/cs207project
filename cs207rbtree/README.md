## cs207rbtree module

This is the cs207rbtree pip installable module. 

* Install: `$ python setup.py install`
* Test: `$ python setup.py test`
* Documentation: `$ python setup.py docs`

There's also a PyPI version that you can download [here](https://pypi.python.org/pypi?%3Aaction=pkg_edit&name=cs207rbtree). Or you can simply run `pip install cs207rbtree` and import in your script.

The module provides interfaces to a *DogBed DataBase*, which is a very simple key-value database working like a dictionary. The underlying data structure is an immutable red-black tree. It persists data by writing to disk.

Here are the sample usage of the module.

```
from cs207rbtree import *

# create and connect a database 
db = connect('test.db')

# set key-value pair
db.set(1) = '1'

# commit changes and write to disk
db.commit()

# get from db
db.get(1) # will return '1'

# close db
db.close()

```
