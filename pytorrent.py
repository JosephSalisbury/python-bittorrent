#!/usr/bin/env python
# pytorrent.py

from bencode import encode, decode
from hashlib import sha1
from urllib import urlencode, urlopen

class Torrent():
	def __init__(self, torrent_file):
		self.data = {}
		self.tracker_response = {}

		# Read and decode the torrent file's contents
		with open(torrent_file) as file:
			self.data = decode(file.read())

	def tracker_request(self):
		# Hash the info file, for the tracker
		info = sha1(encode(self.data["info"])).hexdigest()

		# Generate a tracker GET request.
		payload = {"info_hash" : info,
				"peer_id" : "ABCDEFGHIJKLMNOPQRST",
				"port" : 6969,
				"uploaded" : 0,
				"downloaded" : 0,
				"left" : None}
		payload = urlencode(payload)

		# Send the request
		tracker_url = self.data["announce"]
		response = urlopen(tracker_url + "?" + payload).read()

		self.tracker_response = bencode.decode(response)