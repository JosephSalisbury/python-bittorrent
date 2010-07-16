# bencode.py -- deals with bencoding

# Decode an integer
def decode_int(data):
	try:
		assert data[0] == "i"	# Check it's an integer
		end = data.index('e')	# Find the end of the integer
	except AssertionError, ValueError:
		raise DecodeError("Badly formed argument")

	# Collapse all the tokens together
	t = reduce(lambda x, y: x + y, data[1:end])

	return int(t)			# Integerise it