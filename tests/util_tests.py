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