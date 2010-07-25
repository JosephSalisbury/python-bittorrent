# bencode.py -- deals with bencoding

import types

# Given a compound bencoded expression, starting with a list,
# returns the index of the end of the first list
def walk(exp, index):
	# If it's an integer, find the end, skip to the token after it
	if exp[index] == "i":
		endchar = exp.find("e", index)
		return walk(exp, endchar + 1)

	# If it's a string, collapse the number tokens, then skip that far forward
	elif exp[index].isdigit():
		colon = exp.find(":", index)	# We only want before the first colon
		num = [a for a in exp[index:colon] if a.isdigit() ]
		n = int(collapse(num))

		# Skip the length of the number, the colon, and the length of the string
		return walk(exp, index + len(num) + 1 + n)

	# If it's a sublist, walk through that to the end, then keep going
	elif exp[index] == "l":
		endsublist = walk(exp[index:], 1)
		return walk(exp, index + endsublist)

	elif exp[index] == "d":
		endsubdict = walk(exp[index:], 1)
		return walk(exp, index + endsubdict)

	# If it's a lone "e", jump one to include it, then return
	elif exp[index] == "e":
		index += 1
		return index

# Given a homogenous list l, returns the items of that list concatenated together.
# Eg: collapse(["f", "o", "o"]) == "foo"
def collapse(l):
	return reduce(lambda x, y: x + y, l)

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
		# Take the digits before the colon, and collapse them into an
		# integer.
		colon = exp.find(":")
		num = [a for a in exp[:colon] if a.isdigit() ]
		n = int(collapse(num))	# The length of the string.
		# The string length is the length of the number, colon, and string.
		strlength = len(num) + 1 + n

		x = exp[:strlength]
		xs = inflate(exp[strlength:])

	# The expression starts with a dict, or a list.
	# We can treat both the same way.
	elif ben_type(exp) == list or ben_type(exp) == dict:
		end = walk(exp, 1)	# Find the end of the data type

		x = exp[:end]
		xs = inflate(exp[end:])

	# Returns the first item, with the inflated rest of the list.
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

# Raised if an error occurs during encoding / decoding
class BencodeError(Exception):
	def __init__(self, mode, value, data):
		assert mode in ["Encode", "Decode"]

		self.mode = mode
		self.value = value
		self.data = data

	def __str__(self):
		return repr(self.mode + ": " + self.value + " : " + str(self.data))

# Encode an integer
def encode_int(data):
	try:
		assert type(data) == int
	except AssertionError:
		raise BencodeError("Encode", "Malformed expression", data)

	return "i" + str(data) + "e"

# Decode an integer
def decode_int(data):
	try:
		assert ben_type(data) == int
	except AssertionError:
		raise BencodeError("Decode", "Malformed expression", data)

	try:
		end = data.index("e")	# Find the end of the integer
	except ValueError:
		raise BencodeError("Decode", "Cannot find end of integer expression", data)

	# Remove the substring we want
	t = data[1:end]

	# Quick check for leading zeros, which are not allowed
	if len(t) > 1 and t[0] == "0":
		raise BencodeError("Decode", "Malformed expression, leading zeros", data)

	return int(t)			# Integerise it

# Encode a string
def encode_str(data):
	try:
		assert type(data) == str
	except AssertionError:
		raise BencodeError("Encode", "Malformed expression", data)

	return str(len(data)) + ":" + data

# Decode a string
def decode_str(data):
	try:
		assert ben_type(data) == str
	except AssertionError:
		raise BencodeError("Decode", "Badly formed expression", data)

	# Spin through and collect all the number tokens, before the colon
	try:
		colon = data.find(":")
		num = [a for a in data[:colon] if a.isdigit()]
	except ValueError:
		raise BencodeError("Decode", "Badly formed expression", data)

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
		raise BencodeError("Encode", "Malformed expression", data)

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
		raise BencodeError("Decode", "Malformed expression", data)

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
		raise BencodeError("Encode", "Malformed expression", data)

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
		raise BencodeError("Decode", "Malformed expression", data)

	if data == "de":
		return {}

	data = data[1:-1]

	temp = {}
	terms = inflate(data)

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

# Dispatches data to appropriate encode function
def encode(data):
	try:
		return encode_functions[type(data)](data)
	except KeyError:
		raise BencodeError("Encode", "Unknown data type", data)

# Dispatches data to appropriate decode function
def decode(data):
	try:
		return decode_functions[ben_type(data)](data)
	except KeyError:
		raise BencodeError("Decode", "Unknown data type", data)