#!/usr/bin/env python
# tracker_tests.py -- tests for the bittorrent tracker

import unittest
import tracker
import os
import pickle

class Read_Torrent_DB(unittest.TestCase):
	""" Test that we can read the database correctly. """

	def test_simple_reading(self):
		""" Test that a read works correctly. """

		with open("test.txt", "w") as file:
			pickle.dump("test", file)
		self.n = tracker.read_torrent_db("test.txt")
		self.assertEqual(self.n, "test")
		os.remove("test.txt")

class Write_Torrent_DB(unittest.TestCase):
	""" Test that we can write the database correctly. """

	def test_simple_writing(self):
		""" Test that a write works correctly. """

		tracker.write_torrent_db("test.txt", "test")
		with open("test.txt") as file:
			self.n = pickle.load(file)
		self.assertEqual(self.n, "test")

class Decode_Request(unittest.TestCase):
	""" Test that we can decode GET requests correctly. """

	def test_simple_request(self):
		""" Test that a simple request is decoded correctly. """

		self.n = tracker.decode_request("?key=value")
		self.assertEqual(self.n, {"key":["value"]})

	def test_slash_at_start(self):
		""" Test that if the request has a slash to start, that it is
		removed as well. """

		self.n = tracker.decode_request("/?key=value")
		self.assertEqual(self.n, {"key":["value"]})


unittest.main()