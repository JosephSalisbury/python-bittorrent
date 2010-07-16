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
		
	# Check against leading zeros
	def test6(self):
		self.assertRaises(bencode.DecodeError, bencode.decode_int, list("i04e"))
	
class Decode_String(unittest.TestCase):
	# Check decode works
	def test0(self):
		self.n = bencode.decode_string(list("4:spam"))
		self.assertEqual(self.n, "spam")
			
	def test1(self):
		self.n = bencode.decode_string(list("10:googamoosh"))
		self.assertEqual(self.n, "googamoosh")
		
	def test2(self):
		self.n = bencode.decode_string(list("9:eggandham"))
		self.assertEqual(self.n, "eggandham")
		
	# Check we don't take too much
	def test3(self):
		self.n = bencode.decode_string(list("5:twatstick"))
		self.assertEqual(self.n, "twats")
		
	# Check we raise exceptions for mal-formed expressions
	def test4(self):
		self.assertRaises(bencode.DecodeError, bencode.decode_string, list("nonumber"))
		
	def test5(self):
		self.assertRaises(bencode.DecodeError, bencode.decode_string, list(":::"))
		
class Decode_List(unittest.TestCase):
	def test0(self):
		self.n = bencode.decode_list(list("l4:spam4:eggse"))
		self.assertEqual(self.n, ["spam", "eggs"])
	
unittest.main()