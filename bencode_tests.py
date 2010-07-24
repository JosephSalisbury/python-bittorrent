#!/usr/bin/env python
# bencode_tests.py -- testing the bencoding module

import unittest
import bencode

class Walk(unittest.TestCase):
	""" Check the function walk() works correctly. """

	def test_simple_list(self):
		""" Test that simple lists are correctly seperated. """
		self.exp = "li1eei1e"
		self.n = bencode.walk(self.exp, 1)
		self.assertEqual(self.exp[:self.n], "li1ee")

	def test_longer_list(self):
		""" Test that longer lists are correctly seperated. """
		self.exp = "li1ei2eei1e"
		self.n = bencode.walk(self.exp, 1)
		self.assertEqual(self.exp[:self.n], "li1ei2ee")

	def test_list_with_string(self):
		""" Test that simple list with a string is seperated. """
		self.exp = "l4:teste3:end"
		self.n = bencode.walk(self.exp, 1)
		self.assertEqual(self.exp[:self.n], "l4:teste")

	def test_list_with_long_string(self):
		""" Test a list with a long string is seperated correctly. """
		self.exp = "l10:eggsandhame3:end"
		self.n = bencode.walk(self.exp, 1)
		self.assertEqual(self.exp[:self.n], "l10:eggsandhame")

	def test_nested_list(self):
		""" Test a nested list is seperated correctly. """
		self.exp = "li1eli2eei3eeli1ee"
		self.n = bencode.walk(self.exp, 1)
		self.assertEqual(self.exp[:self.n], "li1eli2eei3ee")

class Collapse(unittest.TestCase):
	""" Check the function collapse() works correctly. """

	def test_concatenation(self):
		""" Test that characters are correctly concatenated. """
		self.n = bencode.collapse(["t", "e", "s", "t"])
		self.assertEqual(self.n, "test")

	def test_exception_raised(self):
		""" Test a TypeError is raised when concating different types. """
		self.assertRaises(TypeError, bencode.collapse, [1, "a", True])

class Inflate(unittest.TestCase):
	""" Check the inflate() function works correctly. """

	def test_simple(self):
		""" Test that a simple expression is inflated correctly. """
		self.n = bencode.inflate("i1e")
		self.assertEqual(self.n, ["i1e"])

	def test_longer(self):
		""" Test that a longer expression is inflated correctly. """
		self.n = bencode.inflate("i1ei2ei3e")
		self.assertEqual(self.n, ["i1e", "i2e", "i3e"])

	def test_mixed(self):
		""" Test that a mixed expression is inflated correctly. """
		self.n = bencode.inflate("3:onei1e3:twoi2e")
		self.assertEqual(self.n, ["3:one", "i1e", "3:two", "i2e"])

class Ben_Type(unittest.TestCase):
	""" Check the function ben_type() works correctly. """

	def test_integers(self):
		""" Test that integers are correctly identified. """
		self.n = bencode.ben_type("i1e")
		self.assertEqual(self.n, int)

	def test_string(self):
		""" Test that strings are correctly identified. """
		self.n = bencode.ben_type("4:test")
		self.assertEqual(self.n, str)

	def test_list(self):
		""" Test that lists are correctly identified. """
		self.n = bencode.ben_type("l4:teste")
		self.assertEqual(self.n, list)

	def test_dict(self):
		""" Test that dictionaries are correctly identified. """
		self.n = bencode.ben_type("d3:key5:valuee")
		self.assertEqual(self.n, dict)

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
	""" Check the function decode_int() works correctly. """

	def test_simple_integers(self):
		""" Test that simple integers are decoded correctly. """
		self.n = bencode.decode_int("i1e")
		self.assertEqual(self.n, 1)

	def test_zero(self):
		""" Test that zero is decoded correctly. """
		self.n = bencode.decode_int("i0e")
		self.assertEqual(self.n, 0)

	def test_longer_integers(self):
		""" Test that longer numbers are correctly decoded. """
		self.n = bencode.decode_int("i12345e")
		self.assertEqual(self.n, 12345)

	def test_minus_integers(self):
		""" Test that minus numbers are correctly decoded. """
		self.n = bencode.decode_int("i-1e")
		self.assertEqual(self.n, -1)

	def test_exception_on_leading_zeros(self):
		""" Test that an exception is raised when decoding an expression which
			has leading zeros. """
		self.assertRaises(bencode.DecodeError, bencode.decode_int, "i01e")

	def test_exception_on_missing_start_constant(self):
		""" Test that an exception is raised when trying to decode an expression
			which is missing the start constant. """
		self.assertRaises(bencode.DecodeError, bencode.decode_int, "1e")

	def test_exception_on_missing_end_constant(self):
		""" Test that an exception is raised when trying to decode an expression
			which is missing the end constant. """
		self.assertRaises(bencode.DecodeError, bencode.decode_int, "i1")

class Encode_Str(unittest.TestCase):
	""" Check the function encode_str() works correctly. """

	def test_character(self):
		""" Test that a single character is encoded correctly. """
		self.n = bencode.encode_str("a")
		self.assertEqual(self.n, "1:a")

	def test_string(self):
		""" Test that a string is encoded correctly. """
		self.n = bencode.encode_str("test")
		self.assertEqual(self.n, "4:test")

	def test_exception_on_int(self):
		""" Test that an exception is raised when trying to encode an integer. """
		self.assertRaises(bencode.EncodeError, bencode.encode_str, 1)

class Decode_Str(unittest.TestCase):
	""" Check the function decode_str() works correctly. """

	def test_character(self):
		""" Test that a single character is decoded correctly """
		self.n = bencode.decode_str("1:a")
		self.assertEqual(self.n, "a")

	def test_string(self):
		""" Test that a string is decoded correctly. """
		self.n = bencode.decode_str("4:test")
		self.assertEqual(self.n, "test")

	def test_string_length(self):
		""" Test that string length is respected. """
		self.n = bencode.decode_str("1:abc")
		self.assertEqual(self.n, "a")

	def test_exception_on_no_number(self):
		""" Test that an exception is raised when no number is prefixed. """
		self.assertRaises(bencode.DecodeError, bencode.decode_str, "abc")

class Encode_List(unittest.TestCase):
	""" Check the function encode_list() works correctly. """

	def test_simple_list(self):
		""" Test that a one item list is encoded correctly. """
		self.n = bencode.encode_list([1])
		self.assertEquals(self.n, "li1ee")

	def test_longer_list(self):
		""" Test that a longer list is encoded correctly. """
		self.n = bencode.encode_list([1, 2, 3])
		self.assertEquals(self.n, "li1ei2ei3ee")

	def test_mixed_list(self):
		""" Test that a mixed list is encoded correctly. """
		self.n = bencode.encode_list([1, "one"])
		self.assertEquals(self.n, "li1e3:onee")

	def test_nested_list(self):
		""" Test that a nested list is encoded correctly. """
		self.n = bencode.encode_list([[1, 2], [3, 4]])
		self.assertEquals(self.n, "lli1ei2eeli3ei4eee")

	def test_empty_list(self):
		""" Test that an empty list is encoded correctly. """
		self.n = bencode.encode_list([])
		self.assertEquals(self.n, "le")

	def test_exception_on_string(self):
		""" Test that an exception is raised when given a string. """
		self.assertRaises(bencode.EncodeError, bencode.encode_list, "test")

class Decode_List(unittest.TestCase):
	""" Check the function decode_list() works correctly. """

	def test_simple_list(self):
		""" Test that a one item list is decoded correctly. """
		self.n = bencode.decode_list("li1ee")
		self.assertEquals(self.n, [1])

	def test_longer_list(self):
		""" Test that a longer list is decoded correctly. """
		self.n = bencode.decode_list("li1ei2ei3ee")
		self.assertEquals(self.n, [1, 2, 3])

	def test_mixed_list(self):
		""" Test that a mixed list is decoded correctly. """
		self.n = bencode.decode_list("li1e3:onee")
		self.assertEquals(self.n, [1, "one"])

	def test_nested_list(self):
		""" Test that a nested list is decoded correctly. """
		self.n = bencode.decode_list("lli1ei2eeli3ei4eee")
		self.assertEquals(self.n, [[1, 2], [3, 4]])

	def test_empty_list(self):
		""" Test that an empty list is decoded correctly. """
		self.n = bencode.decode_list("le")
		self.assertEquals(self.n, [])

	def test_exception_on_string(self):
		""" Test that an exception is raised when given a string. """
		self.assertRaises(bencode.DecodeError, bencode.decode_list, "test")

class Encode_Dict(unittest.TestCase):
	""" Check the function encode_dict() works correctly. """

	def test_simple_dict(self):
		""" Test that a one key dict is encoded correctly. """
		self.n = bencode.encode_dict({"key":"value"})
		self.assertEquals(self.n, "d3:key5:valuee")

	def test_longer_dict(self):
		""" Test that a longer dict is encoded correctly. """
		self.n = bencode.encode_dict({"key_1":"value_1", "key_2":"value_2"})
		self.assertEquals(self.n, "d5:key_17:value_15:key_27:value_2e")

	def test_mixed_dict(self):
		""" Test that a dict with a list value is encoded correctly. """
		self.n = bencode.encode_dict({'key': ['a', 'b']})
		self.assertEquals(self.n, "d3:keyl1:a1:bee")

	def test_nested_dict(self):
		""" Test that a nested dict is encoded correctly. """
		self.n = bencode.encode_dict({"key":{"key":"value"}})
		self.assertEquals(self.n, "d3:keyd3:key5:valueee")

	def test_exception_on_string(self):
		""" Test that an exception is raised when given a string. """
		self.assertRaises(bencode.EncodeError, bencode.encode_dict, "test")

class Encode(unittest.TestCase):
	""" Check the encode() function works. As this dispatches to the other
		encode functions, we only have to check the dispatching, not the other
		functions, as we have already checked those. """

	def test_integers(self):
		""" Test integers are encoded correctly. """
		self.n = bencode.encode(123)
		self.assertEqual(self.n, "i123e")

	def test_strings(self):
		""" Test strings are encoded correctly. """
		self.n = bencode.encode("test")
		self.assertEqual(self.n, "4:test")

	def test_lists(self):
		""" Test lists are encoded correctly. """
		self.n = bencode.encode([1, 2, 3])
		self.assertEquals(self.n, "li1ei2ei3ee")

	def test_dicts(self):
		""" Test dicts are encoded correctly. """
		self.n = bencode.encode({"key":"value"})
		self.assertEquals(self.n, "d3:key5:valuee")

class Decode(unittest.TestCase):
	""" Check the decode() function works. As this dispatches to the other
		decode functions, we only have to check the dispatching, not the other
		functions, as we have already checked those. """

	def test_integers(self):
		self.n = bencode.decode("i123e")
		self.assertEqual(self.n, 123)

	def test_strings(self):
		self.n = bencode.decode("4:test")
		self.assertEqual(self.n, "test")

unittest.main()