#!/usr/bin/env python
# util_tests.py -- testing the util module

import unittest
import util

class Collapse(unittest.TestCase):
	""" Check the function collapse() works correctly. """

	def test_concatenation(self):
		""" Test that characters are correctly concatenated. """

		self.n = util.collapse(["t", "e", "s", "t"])
		self.assertEqual(self.n, "test")

	def test_exception_raised(self):
		""" Test a TypeError is raised when concating different types. """

		self.assertRaises(TypeError, util.collapse, [1, "a", True])

class Slice(unittest.TestCase):
	""" Check the function slice() works correctly. """

	def test_simple(self):
		""" Test that a small string slices correctly. """

		self.n = util.slice("abc", 1)
		self.assertEqual(self.n, ["a", "b", "c"])

	def test_longer(self):
		""" Test that a larger string slice works correctly. """

		self.n = util.slice("abcdef", 2)
		self.assertEqual(self.n, ["ab", "cd", "ef"])

	def test_too_long(self):
		""" Test that a string too long works fine. """

		self.n = util.slice("abcd", 6)
		self.assertEqual(self.n, ["abcd"])