#!/usr/bin/env python
# pytorrent_tests.py -- testing the pytorrent module

import unittest
import pytorrent

class Slice(unittest.TestCase):
	""" Test that the slice() function works correctly. """

	def test_simple(self):
		self.n = pytorrent.slice("abc", 1)
		self.assertEqual(self.n, ["a", "b", "c"])

class Torrent(unittest.TestCase):
	""" Test that that Torrent() class works correctly. """

	def setUp(self):
		""" Read a simple torrent in. """
		self.torrent = pytorrent.Torrent("test.torrent")

	def test_data_present(self):
		""" Test that data is present in the torrent. """
		self.assertTrue(self.torrent.data)

	def tearDown(self):
		""" Remove the torrent. """
		self.torrent = None

unittest.main()