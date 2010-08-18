#!/usr/bin/env python
# tracker_tests.py -- tests for the bittorrent tracker

import unittest
import tracker
import os
import pickle

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

class Add_Peer(unittest.TestCase):
	""" Test that peers are correctly added to the tracker database. """

	def test_unique_peer(self):
		""" Test that a unique peer is added correctly. """

		self.db = {}
		tracker.add_peer(self.db, \
			"test_hash", "test", "100.100.100.100", 1000)
		self.assertEqual(self.db, \
			{'test_hash': [('test', '100.100.100.100', 1000)]})

	def test_duplicate_peer(self):
		""" Test that a duplicated peer is not added. """

		self.db = {'test_hash': [('test', '100.100.100.100', 1000)]}
		tracker.add_peer(self.db, \
			"test_hash", "test", "100.100.100.100", 1000)
		self.assertEqual(self.db, \
			{'test_hash': [('test', '100.100.100.100', 1000)]})

class Make_Compact_Peer_List(unittest.TestCase):
	""" Test that a compact peer list is correctly made. """

	def test_empty_peer(self):
		""" Test that an empty peer list works. """

		self.n = tracker.make_compact_peer_list([])
		self.assertEqual(self.n, "")

	def test_one_peer(self):
		""" Test that one peer works correctly. """

		self.n = tracker.make_compact_peer_list \
			([("test1", "100.100.100.100", "1000")])
		self.assertEqual(self.n, "dddd\x03\xe8")

	def test_multiple_peers(self):
		""" Test that multiple peers works correctly. """

		self.n = tracker.make_compact_peer_list \
			([("test1", "100.100.100.100", "1000"), \
				("test2", "100.100.100.100", "1000")])
		self.assertEqual(self.n, "dddd\x03\xe8dddd\x03\xe8")

class Make_Expanded_Peer_List(unittest.TestCase):
	""" Test that an expanded peer list is correctly made. """

	def test_empty_peer(self):
		""" Test that an empty peer list works correctly. """

		self.n = tracker.make_peer_list([])
		self.assertEqual(self.n, [])

	def test_one_peer(self):
		""" Test that one peer works correctly. """

		self.n = tracker.make_peer_list \
			([("test1", "100.100.100.100", "1000")])
		self.assertEqual(self.n, [{'ip': '100.100.100.100', \
			'peer id': 'test1', 'port': 1000}])

	def test_multiple_peers(self):
		""" Test that multiple peers works correctly. """

		self.n = tracker.make_peer_list \
			([("test1", "100.100.100.100", "1000"), \
				("test2", "100.100.100.100", "1000")])
		self.assertEqual(self.n, [{'ip': '100.100.100.100', \
			'peer id': 'test1', 'port': 1000}, \
				{'ip': '100.100.100.100', \
					'peer id': 'test2', 'port': 1000}])

class Peer_List(unittest.TestCase):
	""" Test that peer_list() dispatcher works correctly. """

	def test_compact_list(self):
		""" Test that a compact peer list dispatches. """

		self.n = tracker.peer_list([("test1", "100.100.100.100", \
			"1000")], True)
		self.assertEqual(self.n, "dddd\x03\xe8")

	def test_expanded_list(self):
		""" Test that an expanded list dispatches. """

		self.n = tracker.peer_list([("test1", "100.100.100.100", \
			"1000")], False)
		self.assertEqual(self.n, [{'ip': '100.100.100.100', \
			'peer id': 'test1', 'port': 1000}])

class Tracker_Test(unittest.TestCase):
	""" Test that the Tracker() class works correctly. """

	def setUp(self):
		""" Start the tracker. """

		self.port = 8888
		self.inmemory = True
		self.interval =10

		self.tracker = tracker.Tracker(port = self.port, \
			inmemory = self.inmemory, \
			interval = self.interval)

	def test_port(self):
		""" Test that the port is correct. """

		self.assertEqual(self.port, self.tracker.port)

	def test_inmemory(self):
		""" Test that inmemory is correct. """

		self.assertEqual(self.inmemory, self.tracker.inmemory)

	def test_interval(self):
		""" Test that the interval is correct. """

		self.assertEqual(self.interval, self.tracker.server_class.interval)

	def tearDown(self):
		""" Stop the tracker. """

		self.tracker = None
