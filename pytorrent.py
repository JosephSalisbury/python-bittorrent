#!/usr/bin/env python
# pytorrent.py

from bencode import encode, decode
from hashlib import sha1
from socket import inet_ntoa
from struct import unpack
from urllib import urlencode, urlopen

def slice(string, n):
	""" Given a string and a number n, cuts the string up, returns a
	list of strings, all size n. """

	temp = []
	i = n
	while i <= len(string):
		temp.append(string[(i-n):i])
		i += n

	return temp

def decode_port(port):
	""" Given a big-endian encoded port, returns the numerical port. """

	return unpack("!H", port)[0]

class Torrent():
	def __init__(self, torrent_file):
		self.data = self.read_torrent_file(torrent_file)
		self.tracker_response = self.make_tracker_request()

	def read_torrent_file(self, torrent_file):
		# Read and decode the torrent file's contents
		with open(torrent_file) as file:
			return decode(file.read())

	def make_tracker_request(self):
		# Hash the info file, for the tracker
		info = self.data["info"]
		info = sha1(encode(info)).digest()

		# Generate a tracker GET request.
		payload = {"info_hash" : info,
				"peer_id" : "ABCDEFGHIJKLMNOPQRST",
				"port" : 6881,
				"uploaded" : 0,
				"downloaded" : 0,
				"left" : 1000,
				"compact" : 0}
		payload = urlencode(payload)

		# Send the request
		tracker_url = self.data["announce"]
		response = urlopen(tracker_url + "?" + payload).read()

		return decode(response)

	def get_peers(self, peers):
		""" Return a list of IPs and ports, given a binary list of
		peers, from a tracker response. """

		peers = slice(peers, 6)	# Cut the response at the end of every peer
		peers = [(inet_ntoa(p[:4]), decode_port(p[4:])) for p in peers]

		return peers

if __name__ == "__main__":
	t = Torrent("test.torrent")
	p = t.get_peers(t.tracker_response["peers"])
	print "PEERS:", p