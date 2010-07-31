#!/usr/bin/env python
# pytorrent_tests.py -- testing the pytorrent module

import unittest
import types
import pytorrent

class Slice(unittest.TestCase):
	""" Test that the slice() function works correctly. """

	def test_simple(self):
		""" Test that a one character slice works. """
		self.n = pytorrent.slice("abc", 1)
		self.assertEqual(self.n, ["a", "b", "c"])

	def test_longer(self):
		""" Test that a longer slice works. """
		self.n = pytorrent.slice("abcdefghi", 3)
		self.assertEqual(self.n, ["abc", "def", "ghi"])

class Decode_Port(unittest.TestCase):
	""" Test that the decode_port() function works correctly. """

	def test(self):
		""" Test that a port is decoded correctly. """
		self.n = pytorrent.decode_port("\x1a\xe1")
		self.assertEqual(self.n, 6881)

class Torrent_Read(unittest.TestCase):
	""" Test that reading torrents works correctly. """

	def test(self):
		""" Test that a torrent file is read correctly. """
		self.n = pytorrent.read_torrent_file("test.torrent")
		# If we have announce, we have read correctly.
		self.assertTrue("announce" in self.n.keys())

class Torrent(unittest.TestCase):
	""" Test that that Torrent() class, et al. works correctly. """

	def setUp(self):
		""" Read a simple torrent in. """
		self.torrent = pytorrent.Torrent("test.torrent")

	def test_data_present(self):
		""" Test that data is present in the torrent. """
		self.assertTrue(self.torrent.data)

	def test_tracker_request(self):
		""" Test that tracker requests work. """
		info = self.torrent.data["info"]
		announce = self.torrent.data["announce"]

		self.n = pytorrent.make_tracker_request(info, announce)
		# If we have peers, the request has worked.
		self.assertTrue("peers" in self.n.keys())

	def test_get_peers(self):
		""" Test that decoding binary peers works. """
		peers = self.torrent.tracker_response["peers"]

		self.peers = pytorrent.get_peers(peers)
		self.assertTrue(type(self.peers) == list)

	def tearDown(self):
		""" Remove the torrent. """
		self.torrent = None

unittest.main()