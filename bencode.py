#	bencode.py -- deals with bencoding
#	Written by Joe Salisbury <salisbury.joseph@gmail.com>
#
#	You are free to use this code in anyway you see fit, on the basis
#	that if it is used, modified, or distributed, proper accreditation
#	of the original author remains.

""" This module deals with the encoding and decoding of bencoded data.
decode() and encode() are the major functions available, to decode
and encode data. """

# Note: Bencoding specification:
# http://www.bittorrent.org/beps/bep_0003.html

import types
from util import collapse

def stringlength(string, index = 0):
	""" Given a bencoded expression, starting with a string, returns
	the length of the string. """

	try:
		colon = string.find(":", index)	# Find the colon, ending the number.
	except ValueError:
		raise BencodeError("Decode", "Malformed expression", data)

	# Return a list of the number characters.
	num = [a for a in string[index:colon] if a.isdigit() ]
	n = int(collapse(num))	# Collapse them, and turn them into an int.

	# Return the length of the number, colon, and the string length.
	return len(num) + 1 + n

def walk(exp, index = 1):
	""" Given a compound bencoded expression, as a string, returns
	the index of the end of the first dict, or list.
	Start at an index of 1, to avoid the start of the actual list. """

	# The expression starts with an integer.
	if exp[index] == "i":
		# Find the end of the integer, then, keep walking.
		endchar = exp.find("e", index)
		return walk(exp, endchar + 1)

	# The expression starts with a string.
	elif exp[index].isdigit():
		# Skip to the end of the string, keep walking.
		strlength = stringlength(exp, index)
		return walk(exp, index + strlength)

	# The expression starts with a list or dict.
	elif exp[index] == "l" or exp[index] == "d":
		# Walk through to the end of the sub, then keep going.
		endsub = walk(exp[index:], 1)
		return walk(exp, index + endsub)

	# The expression is a lone 'e', so we're at the end of the list.
	elif exp[index] == "e":
		index += 1	# Jump one, to include it, then return the index.
		return index

def inflate(exp):
	""" Given a compound bencoded expression, as a string, returns the
	individual data types within the string as items in a list.
	Note, that lists and dicts will come out not inflated. """

	# Base case, for an empty expression.
	if exp == "":
		return []

	# The expression starts with an integer.
	if ben_type(exp) == int:
		# Take the integer, and inflate the rest.
		end = exp.find("e")	# The end of the integer.

		x = exp[:end + 1]
		xs = inflate(exp[end + 1:])

	# The expression starts with a string.
	elif ben_type(exp) == str:
		# Take the string, and inflate the rest.
		strlength = stringlength(exp)	# The end of the string.

		x = exp[:strlength]
		xs = inflate(exp[strlength:])

	# The expression starts with a dict, or a list.
	# We can treat both the same way.
	elif ben_type(exp) == list or ben_type(exp) == dict:
		# Take the sub type, and inflate the rest.
		end = walk(exp)	# Find the end of the data type

		x = exp[:end]
		xs = inflate(exp[end:])

	# Returns the first item, with the inflated rest of the list.
	return [x] + xs

def ben_type(exp):
	""" Given a bencoded expression, returns what type it is. """

	if exp[0] == "i":
		return int
	elif exp[0].isdigit():
		return str
	elif exp[0] == "l":
		return list
	elif exp[0] == "d":
		return dict

def check_type(exp, datatype):
	""" Given an expression, and a datatype, checks the two against
	each other. """

	try:
		assert type(exp) == datatype
	except AssertionError:
		raise BencodeError("Encode", "Malformed expression", exp)

def check_ben_type(exp, datatype):
	""" Given a bencoded expression, and a datatype, checks the two
	against each other. """

	try:
		assert ben_type(exp) == datatype
	except AssertionError:
		raise BencodeError("Decode", "Malformed expression", exp)

class BencodeError(Exception):
	""" Raised if an error occurs encoding or decoding. """

	def __init__(self, mode, value, data):
		""" Takes information of the error. """

		assert mode in ["Encode", "Decode"]

		self.mode = mode
		self.value = value
		self.data = data

	def __str__(self):
		""" Pretty-prints the information. """

		return repr(self.mode + ": " + self.value + " : " + str(self.data))

def encode_int(data):
	""" Given an integer, returns a bencoded string of that integer. """

	check_type(data, int)

	return "i" + str(data) + "e"

def decode_int(data):
	""" Given a bencoded string of a integer, returns the integer. """

	check_ben_type(data, int)

	# Find the end constant of the integer. It may not exist, which would lead
	# to an error being raised.
	try:
		end = data.index("e")
	except ValueError:
		raise BencodeError("Decode", "Cannot find end of integer expression", data)

	t = data[1:end]	# Remove the substring we want.

	# Check for leading zeros, which are not allowed.
	if len(t) > 1 and t[0] == "0":
		raise BencodeError("Decode", "Malformed expression, leading zeros", data)

	return int(t)	# Return an integer.

def encode_str(data):
	""" Given a string, returns a bencoded string of that string. """

	check_type(data, str)

	# Return the length of the string, the colon, and the string itself.
	return str(len(data)) + ":" + data

def decode_str(data):
	""" Given a bencoded string, returns the decoded string. """

	check_ben_type(data, str)

	# We want everything past the first colon.
	try:
		colon = data.find(":")
	except ValueError:
		raise BencodeError("Decode", "Badly formed expression", data)
	# Up to the end of the data.
	strlength = stringlength(data)

	# The subsection of the data we want.
	return data[colon + 1:strlength]

def encode_list(data):
	""" Given a list, returns a bencoded list. """

	check_type(data, list)

	# Special case of an empty list.
	if data == []:
		return "le"

	# Encode each item in the list.
	temp = [encode(item) for item in data]
	# Add list annotation, and collapse the list.
	return "l" + collapse(temp) + "e"

def decode_list(data):
	""" Given a bencoded list, return the unencoded list. """

	check_ben_type(data, list)

	# Special case of an empty list.
	if data == "le":
		return []

	# Remove list annotation, and inflate the l.
	temp = inflate(data[1:-1])
	# Decode each item in the list.
	return [decode(item) for item in temp]

def encode_dict(data):
	""" Given a dictionary, return the bencoded dictionary. """

	check_type(data, dict)

	# Special case of an empty dictionary.
	if data == {}:
		return "de"

	# Encode each key and value for each key in the dictionary.
	temp = [encode_str(key) + encode(data[key]) for key in sorted(data.keys())]
	# Add dict annotation, and collapse the dictionary.
	return "d" + collapse(temp) + "e"

def decode_dict(data):
	""" Given a bencoded dictionary, return the dictionary. """

	check_ben_type(data, dict)

	# Special case of an empty dictionary.
	if data == "de":
		return {}

	# Remove dictionary annotation
	data = data[1:-1]

	temp = {}
	terms = inflate(data)

	# For every key value pair in the terms list, decode the key,
	# and add it to the dictionary, with its decoded value
	count = 0
	while count != len(terms):
		temp[decode_str(terms[count])] = decode(terms[count + 1])
		count += 2

	return temp

# Dictionaries of the data type, and the function to use
encode_functions = { int  : encode_int  ,
					 str  : encode_str  ,
					 list : encode_list ,
					 dict : encode_dict }

decode_functions = { int  : decode_int  ,
					 str  : decode_str  ,
					 list : decode_list ,
					 dict : decode_dict }

def encode(data):
	""" Dispatches data to appropriate encode function. """

	try:
		return encode_functions[type(data)](data)
	except KeyError:
		raise BencodeError("Encode", "Unknown data type", data)

def decode(data):
	""" Dispatches data to appropriate decode function. """

	try:
		return decode_functions[ben_type(data)](data)
	except KeyError:
		raise BencodeError("Decode", "Unknown data type", data)
