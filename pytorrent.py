#!/usr/bin/env python
# pytorrent.py

from bencode import encode, decode
from hashlib import sha1
from random import choice
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

def read_torrent_file(torrent_file):
	""" Given a .torrent file, returns its decoded contents. """

	with open(torrent_file) as file:
		return decode(file.read())

def generate_peer_id():
	""" Returns a 20-byte peer id. """

	# As Azureus style seems most popular, we'll be using that.
	client_id = "PY"
	version_number = "0001"

	# Generate a 12 character long string of random numbers.
	random_string = ""
	while len(random_string) != 12:
		random_string = random_string + choice("1234567890")

	return "-" + client_id + version_number + "-" + random_string

def make_tracker_request(info, peer_id, tracker_url):
	""" Given a torrent info, and tracker_url, returns the tracker
	response. """

	# Generate a tracker GET request.
	payload = {"info_hash" : info,
			"peer_id" : peer_id,
			"port" : 6881,
			"uploaded" : 0,
			"downloaded" : 0,
			"left" : 1000,
			"compact" : 0}
	payload = urlencode(payload)

	# Send the request
	response = urlopen(tracker_url + "?" + payload).read()

	return decode(response)

def get_peers(peers):
	""" Return a list of IPs and ports, given a binary list of
	peers, from a tracker response. """

	peers = slice(peers, 6)	# Cut the response at the end of every peer
	peers = [(inet_ntoa(p[:4]), decode_port(p[4:])) for p in peers]

	return peers

def decode_port(port):
	""" Given a big-endian encoded port, returns the numerical port. """

	return unpack("!H", port)[0]

def generate_handshake(info_hash, peer_id):
	""" Returns a handshake. """

	protocol_id = "BitTorrent protocol"
	len_id = str(len(protocol_id))
	reserved = "00000000"

	return len_id + protocol_id + reserved + info_hash + peer_id

class Torrent():
	def __init__(self, torrent_file):
		self.data = read_torrent_file(torrent_file)

		self.info_hash = sha1(encode(self.data["info"])).digest()
		self.peer_id = generate_peer_id()
		self.handshake = generate_handshake(self.info_hash, self.peer_id)

		self.tracker_response = make_tracker_request(self.info_hash, self.peer_id, self.data["announce"])
		self.peers = get_peers(self.tracker_response["peers"])

if __name__ == "__main__":
	t = Torrent("test.torrent")