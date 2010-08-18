#	simpledb.py -- a nice and simple database
#	Written by Joe Salisbury <salisbury.joseph@gmail.com>
#
#	You are free to use this code in anyway you see fit, on the basis
#	that if it is used, modified, or distributed, proper accreditation
#	of the original author remains.

""" A nice and simple database class. """

# In a nutshell, the Database class acts like a dictionary, and
# implements most of the built-in dictionaries functions. Except its
# persistent!
# As bsddb can only accept strings for keys and values, we need to
# pickle everything before we use it. Therefore, most of the functions
# dump the data, interface with the dict, then load the results.

from bsddb import hashopen
from pickle import dumps, loads

class Database():
	""" A wrapper around a bsddb database, acting as a dictionary.
	Can accept all Python datatypes as keys, and values. """

	def __init__(self, dbname, flag="c"):
		""" Read the database given by dbname. """

		self.data = hashopen(dbname, flag)

	def __contains__(self, key):
		""" Return true if the database contains the key. """

		key = dumps(key)
		boolean = self.data.has_key(key)	# Returns 1 or 0.
		return bool(boolean)

	def __getitem__(self, key):
		""" Return the value held by the key. """

		key = dumps(key)
		value = self.data[key]
		return loads(value)

	def __setitem__(self, key, value):
		""" Set the value of key to the value given. """

		key = dumps(key)
		value = dumps(value)
		self.data[key] = value

	def __repr__(self):
		""" Represent the database. """

		keys = self.data.keys()
		items = [(loads(key), loads(self.data[key])) for key in keys]
		return str(dict(items))

	def clear(self):
		""" Remove all data in the database. """

		self.data.clear()

	def has_key(self, key):
		""" Return true if the database contains the key. """

		return self.__contains__(key)

	def get(self, key):
		""" Return the value held by the key. """

		return self.__getitem__(key)

	def items(self):
		""" Return a list of tuples of the keys and values. """

		keys = self.data.keys()
		items = [(loads(key), loads(self.data[key])) for key in keys]
		return items

	def keys(self):
		""" Return a list of keys. """

		keys = [loads(key) for key in self.data.keys()]
		return keys

	def values(self):
		""" Return a list of values. """

		values = [loads(value) for value in self.data.values()]
		return values

	def pop(self, key):
		""" Return the value given by key, and remove it. """

		key = dumps(key)
		value = self.data[key]
		del self.data[key]
		return loads(value)

	def setdefault(self, key, default):
		""" Return the value held by key, or default if it isn't in
		the database. """

		key = dumps(key)
		try:
			value = self.data[key]
		except KeyError:
			return default
		return loads(value)

	def __del__(self):
		""" Sync the database. """

		self.data.sync()