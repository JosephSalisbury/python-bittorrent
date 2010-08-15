#!/usr/bin/env python
# torrent_tests.py -- testing the torrent module

import unittest
import torrent
import bencode
import hashlib
import os
import util

class Make_Info_Dict(unittest.TestCase):
	""" Test that the make_info_dict function works correctly. """

	def setUp(self):
		""" Write a little file, and turn it into an info dict. """

		self.filename = "test.txt"
		with open(self.filename, "w") as self.file:
			self.file.write("Test file.")
		self.d = torrent.make_info_dict(self.filename)

	def test_length(self):
		""" Test that the length of file is correct. """

		with open(self.filename) as self.file:
			self.length = len(self.file.read())
		self.assertEqual(self.length, self.d["length"])

	def test_name(self):
		""" Test that the name of the file is correct. """

		self.assertEqual(self.filename, self.d["name"])

	def test_md5(self):
		""" Test that the md5 hash of the file is correct. """

		with open(self.filename) as self.file:
			self.md5 = hashlib.md5(self.file.read()).hexdigest()
		self.assertEqual(self.md5, self.d["md5sum"])

	def tearDown(self):
		""" Remove the file. """

		os.remove(self.filename)
		self.d = None

class Make_Torrent_File(unittest.TestCase):
	""" Test that make_torrent_file() works correctly. """

	def setUp(self):
		""" Write a little torrent file. """

		self.filename = "test.txt"
		self.tracker = "http://tracker.com"
		self.comment = "test"
		with open(self.filename, "w") as self.file:
			self.file.write("Test file.")
		self.t = bencode.decode(torrent.make_torrent_file \
			(file = self.filename, \
			tracker = self.tracker, \
			comment = self.comment))

	def test_announce(self):
		""" Test that the announce url is correct. """

		self.assertEqual(self.tracker, self.t["announce"])

	def test_announce_with_multiple_trackers(self):
		""" Test that announce is correct with multiple tracker. """

		self.t = bencode.decode(torrent.make_torrent_file \
			(file = self.filename, \
			tracker = [self.tracker, "http://tracker2.com"], \
			comment = self.comment))
		self.assertEqual(self.tracker, self.t["announce"])

	def test_announce_list(self):
		""" Test that the announce list is correct. """

		self.t = bencode.decode(torrent.make_torrent_file \
			(file = self.filename, \
			tracker = [self.tracker, "http://tracker2.com"], \
			comment = self.comment))
		self.assertEqual([[self.tracker], ["http://tracker2.com"]], \
			self.t["announce-list"])

	def test_created_by(self):
		""" Test that the created by field is correct. """

		self.assertEqual(torrent.CLIENT_NAME, self.t["created by"])

	def test_comment(self):
		""" Test that the comment is correct. """

		self.assertEqual(self.comment, self.t["comment"])

	def test_info_dict(self):
		""" Test that the info dict is correct. """

		self.info = torrent.make_info_dict(self.filename)
		self.assertEqual(self.info, self.t["info"])

	def test_error_on_no_file(self):
		""" Test that an error is raised when no file is given. """

		self.assertRaises(TypeError, torrent.make_torrent_file, \
			tracker = self.tracker)

	def test_error_on_no_tracker(self):
		""" Test that an error is raised when no tracker is given. """

		self.assertRaises(TypeError, torrent.make_torrent_file, \
			file = self.filename)

	def tearDown(self):
		""" Remove the torrent, and the file. """

		os.remove(self.filename)
		self.t = None

class Write_Torrent_File(unittest.TestCase):
	""" Test that write_torrent_file() works. As this dispatches to
	make_torrent_file, we only really need to test for errors, and that
	the actual file exists. """

	def setUp(self):
		""" Write a little torrent file. """

		self.torrent = "testing.torrent"
		self.filename = "test.txt"
		self.tracker = "http://tracker.com"
		self.comment = "test"
		with open(self.filename, "w") as self.file:
			self.file.write("Test file.")
		torrent.write_torrent_file(torrent = self.torrent,  \
			file = self.filename, tracker = self.tracker, \
				comment = self.comment)

	def test_torrent_file(self):
		""" Test that the torrent file has been written to. """

		self.assertTrue(os.path.isfile(self.torrent))

	def test_error_on_no_torrent(self):
		""" Test that an error occurs when no torrent is given. """

		self.assertRaises(TypeError, torrent.write_torrent_file, \
			file = self.filename)

	def tearDown(self):
		""" Remove the file. """

		self.t = None
		os.remove("testing.torrent")

class Read_Torrent_File(unittest.TestCase):
	""" Test that read_torrent_file() works. """

	def setUp(self):
		""" Write a little bencoded data to a file. """

		self.filename = "test.txt"
		self.data = bencode.encode([1, 2, 3])
		with open(self.filename, "w") as self.file:
			self.file.write(self.data)

	def test_read(self):
		""" Test that reading works correctly. """

		self.data = torrent.read_torrent_file(self.filename)
		self.assertEqual(self.data, [1, 2, 3])

	def tearDown(self):
		""" Delete the file. """

		self.data = None
		os.remove(self.filename)

class Generate_Peer_ID(unittest.TestCase):
	""" Test that generate_peer_id() works correctly. """

	def setUp(self):
		""" Generate a peerid. """

		self.peer_id = torrent.generate_peer_id()

	def test_first_dash(self):
		""" Test that the first character is a dash. """

		self.assertEqual("-", self.peer_id[0])

	def test_client_id(self):
		""" Test that the client id is correct. """

		self.assertEqual(torrent.CLIENT_ID, self.peer_id[1:3])

	def test_client_version(self):
		""" Test that the client version is correct. """

		self.assertEqual(torrent.CLIENT_VERSION, self.peer_id[3:7])

	def test_second_dash(self):
		""" Test that the second dash is present. """

		self.assertEqual("-", self.peer_id[7])

	def test_length(self):
		""" Test that the length of the id is correct. """

		self.assertTrue(len(self.peer_id) == 20)

	def tearDown(self):
		""" Remove the peerid. """

		self.peer_id = None

class Decode_Expanded_Peers(unittest.TestCase):
	""" Test that decode_expanded_peers() works. """

	def test_zero_peer(self):
		""" Test that a zero peer list is decoded correctly. """

		self.p = torrent.decode_expanded_peers([])
		self.assertEqual(self.p, [])

	def test_single_peer(self):
		""" Test that a one peer list is decoded. """

		self.p = torrent.decode_expanded_peers( \
			[{'ip': '100.100.100.100', 'peer id': 'test1', \
				'port': 1000}])
		self.assertEqual(self.p, [("100.100.100.100", 1000)])

	def test_multiple_peers(self):
		""" Test that a two peer list is decoded correctly. """

		self.p = torrent.decode_expanded_peers( \
			[{'ip': '100.100.100.100', \
			'peer id': 'test1', 'port': 1000}, \
				{'ip': '100.100.100.100', \
					'peer id': 'test2', 'port': 1000}])
		self.assertEqual(self.p, [('100.100.100.100', 1000), \
			('100.100.100.100', 1000)])

class Decode_Binary_Peers(unittest.TestCase):
	""" Test that decode_binary_peers() works. """

	def test_zero_peer(self):
		""" Test that a zero peer list is decoded correctly. """

		self.p = torrent.decode_binary_peers([])
		self.assertEqual(self.p, [])

	def test_single_peer(self):
		""" Test that a one peer list is decoded. """

		self.p = torrent.decode_binary_peers("dddd\x03\xe8")
		self.assertEqual(self.p, [("100.100.100.100", 1000)])

	def test_multiple_peers(self):
		""" Test that a two peer list is decoded correctly. """

		self.p = torrent.decode_binary_peers("dddd\x03\xe8dddd\x03\xe8")
		self.assertEqual(self.p, [('100.100.100.100', 1000), \
			('100.100.100.100', 1000)])

class Get_Peers(unittest.TestCase):
	""" Test that get_peers() dispatches correctly. """

	def test_binary_list(self):
		""" Test that a binary list is dispatched correctly. """

		self.p = torrent.get_peers("dddd\x03\xe8")
		self.assertEqual(self.p, [("100.100.100.100", 1000)])

	def test_expanded_list(self):
		""" Test that an expanded list is dispatched correctly. """

		self.p = torrent.get_peers( \
			[{'ip': '100.100.100.100', 'peer id': 'test1', \
				'port': 1000}])
		self.assertEqual(self.p, [("100.100.100.100", 1000)])

class Decode_Port(unittest.TestCase):
	""" Test that decode_port() works correctly. """

	def test_port(self):
		""" Test that the port 6881 is decoded correctly. """

		self.p = torrent.decode_port("\x1a\xe1")
		self.assertEqual(self.p, 6881)

class Generate_Handshake(unittest.TestCase):
	""" Test that generate_handshake() works. """

	def setUp(self):
		""" Generate a handshake. """

		self.info_hash = "test_info_hash"
		self.peer_id = "test_peer_id"
		self.h = torrent.generate_handshake(self.info_hash, \
			self.peer_id)

	def test_length_protocol(self):
		""" Test that the length of the protocol is correct. """

		self.assertEqual("19", self.h[0:2])

	def test_protocol_id(self):
		""" Test the protocol id is correct. """

		self.assertEqual("BitTorrent protocol", self.h[2:21])

	def test_reserved(self):
		""" Test that the reserved bytes are correct. """

		self.assertEqual("00000000", self.h[21:29])

	def test_info_hash(self):
		""" Test that the info hash is correct. """

		self.assertEqual(self.info_hash, \
			self.h[29:29+len(self.info_hash)])

	def test_peer_id(self):
		""" Test that the peer id is correct. """

		self.assertEqual(self.peer_id, self.h[29+len(self.info_hash): \
			29+len(self.info_hash)+len(self.peer_id)])

	def tearDown(self):
		""" Remove the handshake. """

		self.h = None