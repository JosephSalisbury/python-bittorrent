#!/usr/bin/env python
# bencode_tests.py -- testing the bencoding module

import unittest
import bencode

class Collapse(unittest.TestCase):
	""" Check the function collapse() works correctly. """

	def test_concatenation(self):
		""" Test that characters are correctly concatenated. """
		self.n = bencode.collapse(["t", "e", "s", "t"])
		self.assertEqual(self.n, "test")

	def test_exception_raised(self):
		""" Test a TypeError is raised when concating different types. """
		self.assertRaises(TypeError, bencode.collapse, [1, "a", True])

class Encode_Int(unittest.TestCase):
	"""  Check the function encode_int() works correctly. """

	def test_simple_integers(self):
		""" Test that simple integers are encoded correctly. """
		self.n = bencode.encode_int(1)
		self.assertEqual(self.n, "i1e")

	def test_zero(self):
		""" Test that zero is encoded correctly. """
		self.n = bencode.encode_int(0)
		self.assertEqual(self.n, "i0e")

	def test_longer_integers(self):
		""" Test that longer numbers are correctly encoded. """
		self.n = bencode.encode_int(12345)
		self.assertEqual(self.n, "i12345e")

	def test_minus_integers(self):
		""" Test that minus numbers are correctly encoded. """
		self.n = bencode.encode_int(-1)
		self.assertEqual(self.n, "i-1e")

	def test_leading_zeros(self):
		""" Test that leading zeros are correctly removed. """
		self.n = bencode.encode_int(01)
		self.assertEqual(self.n, "i1e")

	def test_exception_on_string(self):
		""" Test an exception is raised when encoding a string. """
		self.assertRaises(bencode.EncodeError, bencode.encode_int, "test")

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

class Encode_Str(unittest.TestCase):
	# Check encode works
	def test0(self):
		self.n = bencode.encode_str("spam")
		self.assertEqual(self.n, "4:spam")

	def test1(self):
		self.n = bencode.encode_str("googamoosh")
		self.assertEqual(self.n, "10:googamoosh")

	def test2(self):
		self.n = bencode.encode_str("eggandham")
		self.assertEqual(self.n, "9:eggandham")

	# Check exceptions are properly raised
	def test3(self):
		self.assertRaises(bencode.EncodeError, bencode.encode_str, 5)

	def test4(self):
		self.assertRaises(bencode.EncodeError, bencode.encode_str, 100)

class Decode_Str(unittest.TestCase):
	# Check decode works
	def test0(self):
		self.n = bencode.decode_str("4:spam")
		self.assertEqual(self.n, "spam")

	def test1(self):
		self.n = bencode.decode_str("10:googamoosh")
		self.assertEqual(self.n, "googamoosh")

	def test2(self):
		self.n = bencode.decode_str("9:eggandham")
		self.assertEqual(self.n, "eggandham")

	# Check we don't take too much
	def test3(self):
		self.n = bencode.decode_str("5:twatstick")
		self.assertEqual(self.n, "twats")

	# Check we raise exceptions for mal-formed expressions
	def test4(self):
		self.assertRaises(bencode.DecodeError, bencode.decode_str, "nonumber")

	def test5(self):
		self.assertRaises(bencode.DecodeError, bencode.decode_str, ":::")

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

class Encode_Dict(unittest.TestCase):
	# Check encode works
	def test0(self):
		self.n = bencode.encode_dict({"cow":"moo", "spam":"eggs"})
		self.assertEquals(self.n, "d3:cow3:moo4:spam4:eggse")

	def test1(self):
		self.n = bencode.encode_dict({"3": "three"})
		self.assertEquals(self.n, "d1:35:threee")

	def test2(self):
		self.n = bencode.encode_dict({'spam': ['a', 'b']})
		self.assertEquals(self.n, "d4:spaml1:a1:bee")

	def test3(self):
		self.n = bencode.encode_dict({"sub":{"foo":"bar"}})
		self.assertEquals(self.n, "d3:subd3:foo3:baree")

	# Check exceptions are raised
	def test4(self):
		self.assertRaises(bencode.EncodeError, bencode.encode_dict, "notadictionary")

	def test5(self):
		self.assertRaises(bencode.EncodeError, bencode.encode_dict, 456)

class Encode(unittest.TestCase):
	# Check encode works, on ints
	def test0(self):
		self.n = bencode.encode(2)
		self.assertEqual(self.n, "i2e")

	def test1(self):
		self.n = bencode.encode(0)
		self.assertEqual(self.n, "i0e")

	def test2(self):
		self.n = bencode.encode(-9)
		self.assertEqual(self.n, "i-9e")

	# Check encode works on strings
	def test3(self):
		self.n = bencode.encode("spam")
		self.assertEqual(self.n, "4:spam")

	def test4(self):
		self.n = bencode.encode("eggandham")
		self.assertEqual(self.n, "9:eggandham")

	def test5(self):
		self.n = bencode.encode("jacky")
		self.assertEqual(self.n, "5:jacky")

	# Check encode works on lists
	def test6(self):
		self.n = bencode.encode(["spam", "eggs"])
		self.assertEquals(self.n, "l4:spam4:eggse")

	def test7(self):
		self.n = bencode.encode([1, 2, 3])
		self.assertEquals(self.n, "li1ei2ei3ee")

	def test8(self):
		self.n = bencode.encode([[1, 2], [3, 4]])
		self.assertEquals(self.n, "lli1ei2eeli3ei4eee")

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