# bencode.py -- deals with bencoding

# Raised if an error occurs decoding, typically malformed expressions
class DecodeError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

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

	# Reduce the number tokens into one integer
	n = int(reduce(lambda x, y: x + y, num))

	# The reduction of the string we want
	t = data[lenNum:n+lenNum]

	return t

# Dispatches data to appropriate decode_* function
def decode(data):
	if data[0] == "i":
		return decode_int(data)
	elif data[0].isdigit():
		return decode_string(data)
	else:
		raise DecodeError("Badly formed expression.")