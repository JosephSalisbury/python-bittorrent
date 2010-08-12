#!/usr/bin/env python
# tracker_tests.py -- tests for the bittorrent tracker

import unittest
import tracker
import os
import pickle

class Read_Torrent_DB(unittest.TestCase):
	""" Test that we can read the database correctly. """

	def test_reading(self):
		""" Test that a read works correctly. """
		with open("test.txt", "w") as file:
			pickle.dump("test", file)
		self.n = tracker.read_torrent_db("test.txt")
		self.assertEqual(self.n, "test")
		os.remove("test.txt")

class Write_Torrent_DB(unittest.TestCase):
	""" Test that we can write the database correctly. """

	def test_writing(self):
		tracker.write_torrent_db("test.txt", "test")
		with open("test.txt") as file:
			self.n = pickle.load(file)
		self.assertEqual(self.n, "test")

unittest.main()