#!/usr/bin/env python
# simpledb_tests.py -- tests for simpledb.py

import unittest
import simpledb

class Database_Tests(unittest.TestCase):
	""" Test that the Database() class works correctly. """

	def setUp(self):
		self.db = simpledb.Database(None)
		self.db["key"] = "value"	# Test key, value pair

	def test_contains(self):
		self.assertTrue(self.db.__contains__("key"))

	def test_getitem(self):
		self.assertEqual(self.db.__getitem__("key"), "value")

	def test_setitem(self):
		self.db.__setitem__("test_key", "test_value")
		self.assertEqual(self.db["test_key"], "test_value")

	def test_clear(self):
		self.db.clear()
		self.assertEqual(self.db.data, {})

	def test_has_key(self):
		self.assertTrue(self.db.has_key("key"))

	def test_get(self):
		self.assertEqual(self.db.get("key"), "value")

	def test_items(self):
		self.assertEqual(self.db.items(), [("key", "value")])

	def test_keys(self):
		self.assertEqual(self.db.keys(), ["key"])

	def test_values(self):
		self.assertEqual(self.db.values(), ["value"])

	def test_pop_return(self):
		self.assertEqual(self.db.pop("key"), "value")

	def test_pop_delete(self):
		self.db.pop("key")
		self.assertEqual(self.db.data, {})

	def test_setdefault_get(self):
		self.assertEqual(self.db.setdefault("key", "def"), "value")

	def test_setdefault_default(self):
		self.assertEqual(self.db.setdefault("no_key", "def"), "def")

	def tearDown(self):
		self.db = None