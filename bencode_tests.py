#!/usr/bin/env python
# bencode_tests.py -- testing the bencoding module

import unittest
import bencode

class Encode_Int(unittest.TestCase):
	# Check encode works
	def test0(self):
		self.n = bencode.encode_int(2)
		self.assertEqual(self.n, "i2e")

	def test1(self):
		self.n = bencode.encode_int(0)
		self.assertEqual(self.n, "i0e")

	def test2(self):
		self.n = bencode.encode_int(456)
		self.assertEqual(self.n, "i456e")

	# Check exceptions are raised for bad expressions
	def test3(self):
		self.assertRaises(bencode.EncodeError, bencode.encode_int, "459e")

	def test4(self):
		self.assertRaises(bencode.EncodeError, bencode.encode_int, "i459")

	def test5(self):
		self.assertRaises(bencode.EncodeError, bencode.encode_int, "googamoosh")

class Decode_Int(unittest.TestCase):
	# Check decode works
	def test0(self):
		self.n = bencode.decode_int("i2e")
		self.assertEqual(self.n, 2)

	def test1(self):
		self.n = bencode.decode_int("i0e")
		self.assertEqual(self.n, 0)

	def test2(self):
		self.n = bencode.decode_int("i456e")
		self.assertEqual(self.n, 456)

	# Check exceptions are raised for bad expressions
	def test3(self):
		self.assertRaises(bencode.DecodeError, bencode.decode_int, "459e")

	def test4(self):
		self.assertRaises(bencode.DecodeError, bencode.decode_int, "i459")

	def test5(self):
		self.assertRaises(bencode.DecodeError, bencode.decode_int, "googamoosh")

	# Check against leading zeros
	def test6(self):
		self.assertRaises(bencode.DecodeError, bencode.decode_int, "i04e")

class Encode_String(unittest.TestCase):
	# Check encode works
	def test0(self):
		self.n = bencode.encode_string("spam")
		self.assertEqual(self.n, "4:spam")

	def test1(self):
		self.n = bencode.encode_string("googamoosh")
		self.assertEqual(self.n, "10:googamoosh")

	def test2(self):
		self.n = bencode.encode_string("eggandham")
		self.assertEqual(self.n, "9:eggandham")

	# Check exceptions are properly raised
	def test3(self):
		self.assertRaises(bencode.EncodeError, bencode.encode_string, 5)

	def test4(self):
		self.assertRaises(bencode.EncodeError, bencode.encode_string, 100)

class Decode_String(unittest.TestCase):
	# Check decode works
	def test0(self):
		self.n = bencode.decode_string("4:spam")
		self.assertEqual(self.n, "spam")

	def test1(self):
		self.n = bencode.decode_string("10:googamoosh")
		self.assertEqual(self.n, "googamoosh")

	def test2(self):
		self.n = bencode.decode_string("9:eggandham")
		self.assertEqual(self.n, "eggandham")

	# Check we don't take too much
	def test3(self):
		self.n = bencode.decode_string("5:twatstick")
		self.assertEqual(self.n, "twats")

	# Check we raise exceptions for mal-formed expressions
	def test4(self):
		self.assertRaises(bencode.DecodeError, bencode.decode_string, "nonumber")

	def test5(self):
		self.assertRaises(bencode.DecodeError, bencode.decode_string, ":::")

class Encode_List(unittest.TestCase):
	# Check encode works
	def test0(self):
		self.n = bencode.encode_list(["spam", "eggs"])
		self.assertEquals(self.n, "l4:spam4:eggse")

	def test1(self):
		self.n = bencode.encode_list([1, 2, 3])
		self.assertEquals(self.n, "li1ei2ei3ee")

	def test2(self):
		self.n = bencode.encode_list(["one", 1])
		self.assertEquals(self.n, "l3:onei1ee")

	def test3(self):
		self.n = bencode.encode_list([[1, 2], [3, 4]])
		self.assertEquals(self.n, "lli1ei2eeli3ei4eee")

	# Check exceptions are raised
	def test4(self):
		self.assertRaises(bencode.EncodeError, bencode.encode_list, "nonumber")

	def test5(self):
		self.assertRaises(bencode.EncodeError, bencode.encode_list, "400")

class Encode(unittest.TestCase):
	# Check encode works
	def test0(self):
		self.n = bencode.encode(2)
		self.assertEqual(self.n, "i2e")

	def test1(self):
		self.n = bencode.encode(0)
		self.assertEqual(self.n, "i0e")

	def test2(self):
		self.n = bencode.encode(-9)
		self.assertEqual(self.n, "i-9e")

	def test3(self):
		self.n = bencode.encode("spam")
		self.assertEqual(self.n, "4:spam")

	def test4(self):
		self.n = bencode.encode("eggandham")
		self.assertEqual(self.n, "9:eggandham")

class Decode(unittest.TestCase):
	# Check decode works
	def test0(self):
		self.n = bencode.decode("i2e")
		self.assertEqual(self.n, 2)

	def test1(self):
		self.n = bencode.decode("i0e")
		self.assertEqual(self.n, 0)

	def test2(self):
		self.n = bencode.decode("4:spam")
		self.assertEqual(self.n, "spam")

	def test3(self):
		self.n = bencode.decode("9:eggandham")
		self.assertEqual(self.n, "eggandham")

	# Check exceptions are correctly raised
	def test4(self):
		self.assertRaises(bencode.DecodeError, bencode.decode, "i459")

	def test5(self):
		self.assertRaises(bencode.DecodeError, bencode.decode, "nonumber")

unittest.main()