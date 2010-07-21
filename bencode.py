# bencode.py -- deals with bencoding

import types

# Given a homogenous list l, returns the items of that list concatenated together.
# Eg: collapse(["f", "o", "o"]) == "foo"
def collapse(l):
	return reduce(lambda x, y: x + y, l)

# Raised if an error occurs encoding.
class EncodeError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

# Raised if an error occurs decoding, typically malformed expressions
class DecodeError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

# Encode an integer
def encode_int(num):
	try:
		assert type(num) == int
	except AssertionError:
		raise EncodeError("Malformed expression.")

	return "i" + str(num) + "e"

# Decode an integer
def decode_int(data):
	try:
		assert data[0] == "i"	# Check it's an integer
		end = data.index('e')	# Find the end of the integer
	except AssertionError:
		raise DecodeError("Badly formed expression.")
	except ValueError:
		raise DecodeError("Cannot find end of expression.")

	# Remove the substring we want
	t = data[1:end]

	# Quick check for leading zeros, which are not allowed
	if len(t) > 1 and t[0] == "0":
		raise DecodeError("Malformed expression, leading zeros")

	return int(t)			# Integerise it

# Encode a string
def encode_string(data):
	try:
		assert type(data) == str
	except AssertionError:
		raise EncodeError("Malformed expression.")

	return str(len(data)) + ":" + data

# Decode a string
def decode_string(data):
	try:
		assert data[0].isdigit() == True
	except AssertionError:
		raise DecodeError("Badly formed expression.")

	# Spin through, collect the number tokens, and count them
	num = []	# The tokens of the number
	lenNum = 1	# How many digits in the number
	for x in data:
		if x.isdigit():
			num.append(x)
			lenNum += 1
		else:
			break

	# Reduce the number characters into one string, then integerise it
	n = int(collapse(num))

	# The subsection of the string we want
	t = data[lenNum:n+lenNum]

	return t

# Encode a list
def encode_list(data):
	try:
		assert type(data) == list
	except AssertionError:
		raise EncodeError("Malformed expression.")

	temp = []
	for item in data:
		temp.append(encode(item))

	return "l" + collapse(temp) + "e"

# Decode a list
def decode_list(data):
	pass

# Encode a dictionary
def encode_dict(data):
	try:
		assert type(data) == dict
	except AssertionError:
		raise EncodeError("Malformed expression.")

	temp = []
	for key in sorted(data.keys()):
		temp.append(encode_string(key))	# Keys must be strings
		temp.append(encode(data[key]))

	return "d" + collapse(temp) + "e"

# Decode a dictionary
def decode_dict(data):
	pass

# Dispatches data to appropriate encode function
def encode(data):
	if type(data) == int:
		return encode_int(data)
	elif type(data) == str:
		return encode_string(data)
	elif type(data) == list:
		return encode_list(data)
	elif type(data) == dict:
		return encode_dict(data)
	else:
		raise EncodeError("Unknown data type")

# Dispatches data to appropriate decode function
def decode(data):
	if data[0] == "i":
		return decode_int(data)
	elif data[0].isdigit():
		return decode_string(data)
	else:
		raise DecodeError("Unknown data type.")