#!/usr/bin/env python
# simpledb_tests.py -- tests for simpledb.py

import unittest
import simpledb

class Database_Tests(unittest.TestCase):
	""" Test that the Database() class works correctly. """

	def setUp(self):
		self.db = simpledb.Database("testingdb")

	def tearDown(self):
		self.db = None