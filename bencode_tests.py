#!/usr/bin/env python
# bencode_tests.py -- testing the bencoding module

import unittest
import bencode

class Decode_Int(unittest.TestCase):
	def test0(self):
		t = list("i2e")
		n = bencode.decode_int(t)

		assert(n == 2)

	def test1(self):
		t = list("i0e")
		n = bencode.decode_int(t)

		assert(n == 0)

	def test2(self):
		t = list("i456e")
		n = bencode.decode_int(t)

		assert(n == 456)

unittest.main()