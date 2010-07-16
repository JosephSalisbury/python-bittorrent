# bencode.py -- deals with bencoding

# Decode an integer
def decode_int(data):
	assert data[0] == "i"	# Check it's an integer

	end = data.index('e')
	t = reduce(lambda x, y: x + y, data[1:end])

	return int(t)