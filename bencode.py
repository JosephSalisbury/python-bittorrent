# bencode.py -- deals with bencoding

import types

# Given a compound bencoded expression, starting with a list,
# returns the index of the end of the first list
def list_walk(exp, index):
	# If it's an integer, find the end, skip to the token after it
	if exp[index] == "i":
		endchar = exp.find("e", index)
		return list_walk(exp, endchar + 1)

	# If it's a string, collapse the number tokens, then skip that far forward
	elif exp[index].isdigit():
		num = []
		for x in exp[index:]:
			if x.isdigit():
				num.append(x)
			else:
				break
		n = int(collapse(num))

		# Skip the number of characters, the length of it, and the colon
		return list_walk(exp, index + n + len(num) + 1)

	# If it's a sublist, walk through that to the end, then keep going
	elif exp[index] == "l":
		endsublist = list_walk(exp[index:], 1)
		return list_walk(exp, index + endsublist)

	# If it's a lone "e", jump one to include it, then return
	elif exp[index] == "e":
		index += 1
		return index

# Given a homogenous list l, returns the items of that list concatenated together.
# Eg: collapse(["f", "o", "o"]) == "foo"
def collapse(l):
	return reduce(lambda x, y: x + y, l)

def inflate(exp):
	if exp == "":
		return []

	if ben_type(exp) == int:
		end = exp.find("e")
		# The length of the integer is the same as the index of the ending character
		# This means its the only integer in the expression, and we just return it
		if end == len(exp) - 1:
			return [exp]
		else:
		# Otherwise, take the first integer, and inflate the rest
			x = exp[:end + 1]
			xs = inflate( exp[end + 1: ] )

			return [x] + xs

	elif ben_type(exp) == str:
		if len(exp) == int(exp[0]) + 2:
			return [exp]
		else:
			strlength = int(exp[0])

			x = exp[:strlength + 2]
			xs = inflate ( exp[strlength+ 2: ])

			return [x] + xs

	elif ben_type(exp) == list:
		if len(exp) == 2:	# Just an empty list
			return [exp]
		else:
			endlist = list_walk(exp, 1)

			x = exp[:endlist]
			xs = inflate( exp[endlist:] )

			return [x] + xs

# Given a bencoded expression, returns what type it is
#Eg: ben_type("i1e") == "int"
def ben_type(expression):
	if expression[0] == "i":
		return int
	elif expression[0].isdigit():
		return str
	elif expression[0] == "l":
		return list
	elif expression[0] == "d":
		return dict

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
def encode_int(data):
	try:
		assert type(data) == int
	except AssertionError:
		raise EncodeError("Malformed expression.")

	return "i" + str(data) + "e"

# Decode an integer
def decode_int(data):
	try:
		assert ben_type(data) == int
	except AssertionError:
		raise DecodeError("Malformed expression.")

	try:
		end = data.index("e")	# Find the end of the integer
	except ValueError:
		raise DecodeError("Cannot find end of integer expression.")

	# Remove the substring we want
	t = data[1:end]

	# Quick check for leading zeros, which are not allowed
	if len(t) > 1 and t[0] == "0":
		raise DecodeError("Malformed expression, leading zeros")

	return int(t)			# Integerise it

# Encode a string
def encode_str(data):
	try:
		assert type(data) == str
	except AssertionError:
		raise EncodeError("Malformed expression.")

	return str(len(data)) + ":" + data

# Decode a string
def decode_str(data):
	try:
		assert ben_type(data) == str
	except AssertionError:
		raise DecodeError("Badly formed expression.")

	# Spin through and collect all the number tokens
	num = []	# The tokens of the number
	for x in data:
		if x.isdigit():
			num.append(x)
		else:
			break

	# Reduce the number characters into one string, then integerise it
	n = int(collapse(num))

	lenNum = len(num) + 1	# Including the colon, as well
	# The subsection of the string we want
	t = data[lenNum:n+lenNum]

	return t

# Encode a list
def encode_list(data):
	try:
		assert type(data) == list
	except AssertionError:
		raise EncodeError("Malformed expression.")

	if data == []:
		return "le"

	temp = []
	for item in data:
		temp.append(encode(item))

	return "l" + collapse(temp) + "e"

# Decode a list
def decode_list(data):
	try:
		assert ben_type(data) == list
	except AssertionError:
		raise DecodeError("Malformed expression.")

	if data == "le":
		return []

	data = data[1:-1]	# Remove the list annotation

	temp = []
	for item in inflate(data):
		temp.append(decode(item))

	return temp

# Encode a dictionary
def encode_dict(data):
	try:
		assert type(data) == dict
	except AssertionError:
		raise EncodeError("Malformed expression.")

	if data == {}:
		return "de"

	temp = []
	for key in sorted(data.keys()):
		temp.append(encode_str(key))	# Keys must be strings
		temp.append(encode(data[key]))

	return "d" + collapse(temp) + "e"

# Decode a dictionary
def decode_dict(data):
	try:
		assert ben_type(data) == dict
	except AssertionError:
		raise DecodeError("Malformed expression.")

	if data == "de":
		return {}

	data = data[1:-1]

	temp = {}
	for item in inflate(data):
		# Add to the dictionary
		pass

	return temp

# Dictionaries of the data type, and the function to use
encode_functions = {int:encode_int,
					str:encode_str,
					list:encode_list,
					dict:encode_dict}

decode_functions = {int:decode_int,
					str:decode_str,
					list:decode_list,
					dict:decode_dict}

# Dispatches data to appropriate encode function
def encode(data):
	try:
		return encode_functions[type(data)](data)
	except KeyError:
		raise EncodeError("Unknown data type.")

# Dispatches data to appropriate decode function
def decode(data):
	try:
		return decode_functions[ben_type(data)](data)
	except KeyError:
		raise DecodeError("Unknown data type.")