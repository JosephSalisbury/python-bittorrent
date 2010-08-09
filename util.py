# util.py
# A small collection of useful functions

def collapse(data):
	""" Given an homogenous list, returns the items of that list
	concatenated together. """

	return reduce(lambda x, y: x + y, data)

def slice(string, n):
	""" Given a string and a number n, cuts the string up, returns a
	list of strings, all size n. """

	temp = []
	i = n
	while i <= len(string):
		temp.append(string[(i-n):i])
		i += n

	try:	# Add on any stragglers
		if string[(i-n)] != "":
			temp.append(string[(i-n):])
	except IndexError:
		pass

	return temp