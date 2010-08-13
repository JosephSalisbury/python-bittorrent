#!/usr/bin/env python
# torrent_tests.py -- testing the torrent module

import unittest
import torrent
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