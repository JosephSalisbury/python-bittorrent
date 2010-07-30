#!/usr/bin/env python
# pytorrent_tests.py -- testing the pytorrent module

import unittest
import pytorrent

class Torrent(unittest.TestCase):
	""" Test that that Torrent() class works correctly. """

	def setUp(self):
		""" Read a simple torrent in. """
		self.torrent = pytorrent.Torrent("test.torrent")

	def test_error_on_no_torrent(self):
		""" Test that an error is raised when no torrent is present. """
		self.assertRaises(IOError, pytorrent.Torrent.read_torrent_file, "nofile.torrent")

	def test_data_present(self):
		""" Test that data is present in the torrent. """
		self.assertTrue(self.torrent.data)

	def tearDown(self):
		""" Remove the torrent. """
		self.torrent = None

unittest.main()