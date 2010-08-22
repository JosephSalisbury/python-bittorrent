# torrent.py
# Torrent file related utilities

from hashlib import md5, sha1
from random import choice
import socket
from struct import pack, unpack
from threading import Thread
from time import sleep, time
import types
from urllib import urlencode, urlopen
from util import collapse, slice

from bencode import decode, encode
from btexceptions import NetworkError

CLIENT_NAME = "pytorrent"
CLIENT_ID = "PY"
CLIENT_VERSION = "0001"

def make_info_dict(file):
	""" Returns the info dictionary for a torrent file. """

	with open(file) as f:
		contents = f.read()

	piece_length = 524288	# TODO: This should change dependent on file size

	info = {}

	info["piece length"] = piece_length
	info["length"] = len(contents)
	info["name"] = file
	info["md5sum"] = md5(contents).hexdigest()

	# Generate the pieces
	pieces = slice(contents, piece_length)
	pieces = [ sha1(p).digest() for p in pieces ]
	info["pieces"] = collapse(pieces)

	return info

def make_torrent_file(file = None, tracker = None, comment = None):
	""" Returns the bencoded contents of a torrent file. """

	if not file:
		raise TypeError("make_torrent_file requires at least one file, non given.")
	if not tracker:
		raise TypeError("make_torrent_file requires at least one tracker, non given.")

	torrent = {}

	# We only have one tracker, so that's the announce
	if type(tracker) != list:
		torrent["announce"] = tracker
	# Multiple trackers, first is announce, and all go in announce-list
	elif type(tracker) == list:
		torrent["announce"] = tracker[0]
		# And for some reason, each needs its own list
		torrent["announce-list"] = [[t] for t in tracker]

	torrent["creation date"] = int(time())
	torrent["created by"] = CLIENT_NAME
	if comment:
		torrent["comment"] = comment

	torrent["info"] = make_info_dict(file)

	return encode(torrent)

def write_torrent_file(torrent = None, file = None, tracker = None, \
	comment = None):
	""" Largely the same as make_torrent_file(), except write the file
	to the file named in torrent. """

	if not torrent:
		raise TypeError("write_torrent_file() requires a torrent filename to write to.")

	data = make_torrent_file(file = file, tracker = tracker, \
		comment = comment)
	with open(torrent, "w") as torrent_file:
		torrent_file.write(data)

def read_torrent_file(torrent_file):
	""" Given a .torrent file, returns its decoded contents. """

	with open(torrent_file) as file:
		return decode(file.read())

def generate_peer_id():
	""" Returns a 20-byte peer id. """

	# As Azureus style seems most popular, we'll be using that.
	# Generate a 12 character long string of random numbers.
	random_string = ""
	while len(random_string) != 12:
		random_string = random_string + choice("1234567890")

	return "-" + CLIENT_ID + CLIENT_VERSION + "-" + random_string

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
			"compact" : 1}
	payload = urlencode(payload)

	# Send the request
	response = urlopen(tracker_url + "?" + payload).read()

	return decode(response)

def decode_expanded_peers(peers):
	""" Return a list of IPs and ports, given an expanded list of peers,
	from a tracker response. """

	return [(p["ip"], p["port"]) for p in peers]

def decode_binary_peers(peers):
	""" Return a list of IPs and ports, given a binary list of peers,
	from a tracker response. """

	peers = slice(peers, 6)	# Cut the response at the end of every peer
	return [(socket.inet_ntoa(p[:4]), decode_port(p[4:])) for p in peers]

def get_peers(peers):
	""" Dispatches peer list to decode binary or expanded peer list. """

	if type(peers) == str:
		return decode_binary_peers(peers)
	elif type(peers) == list:
		return decode_expanded_peers(peers)

def decode_port(port):
	""" Given a big-endian encoded port, returns the numerical port. """

	return unpack(">H", port)[0]

def generate_handshake(info_hash, peer_id):
	""" Returns a handshake. """

	protocol_id = "BitTorrent protocol"
	len_id = str(len(protocol_id))
	reserved = "00000000"

	return len_id + protocol_id + reserved + info_hash + peer_id

def send_recv_handshake(handshake, host, port):
	""" Sends a handshake, returns the data we get back. """

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, port))
	s.send(handshake)

	data = s.recv(len(handshake))
	s.close()

	return data

class Torrent():
	def __init__(self, torrent_file):
		self.running = False

		self.data = read_torrent_file(torrent_file)

		self.info_hash = sha1(encode(self.data["info"])).digest()
		self.peer_id = generate_peer_id()
		self.handshake = generate_handshake(self.info_hash, self.peer_id)

	def perform_tracker_request(self, url, info_hash, peer_id):
		""" Make a tracker request to url, every interval seconds, using
		the info_hash and peer_id, and decode the peers. """

		while self.running:
			self.tracker_response = make_tracker_request(info_hash, peer_id, url)

			if "failure reason" not in self.tracker_response:
				self.peers = get_peers(self.tracker_response["peers"])
			sleep(self.tracker_response["interval"])

	def run(self):
		""" Start the torrent running. """

		if not self.running:
			self.running = True

			self.tracker_loop = Thread(target = self.perform_tracker_request, \
				args = (self.data["announce"], self.info_hash, self.peer_id))
			self.tracker_loop.start()

	def stop(self):
		""" Stop the torrent from running. """

		if self.running:
			self.running = False

			self.tracker_loop.join()

