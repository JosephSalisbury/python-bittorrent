# bencode.py -- deals with bencoding

# Access point for decoding
def decode(data):
	tokens = list(data)		# Listify the data
	main(tokens)			# Send it to the main decoder

# Decode a dictionary
def decode_dict(data):
	assert data[0] == "d"	# Check it's a dictionary

	data.pop()

	print data[:100]

# Work out what to decode, then dispatch it
def main(data):
	if data[0] == "d":
		decode_dict(data)