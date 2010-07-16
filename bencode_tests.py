#!/usr/bin/env python
# bencode_tests.py -- testing the bencoding module

import unittest
import bencode

class Decode_Int(unittest.TestCase):
	# Check decode works
	def test0(self):
		self.n = bencode.decode_int(list("i2e"))
		self.assertEqual(self.n, 2)

	def test1(self):
		self.n = bencode.decode_int(list("i0e"))
		self.assertEqual(self.n, 0)

	def test2(self):
		self.n = bencode.decode_int(list("i456e"))
		self.assertEqual(self.n, 456)

	# Check exceptions are raised for bad expressions
	def test3(self):
		self.assertRaises(bencode.DecodeError, bencode.decode_int, list("459e"))

	def test4(self):
		self.assertRaises(bencode.DecodeError, bencode.decode_int, list("i459"))

	def test5(self):
		self.assertRaises(bencode.DecodeError, bencode.decode_int, list("googamoosh"))

unittest.main()