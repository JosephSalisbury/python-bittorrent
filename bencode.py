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

	# Collapse all the tokens together
	t = reduce(lambda x, y: x + y, data[1:end])

	return int(t)			# Integerise it