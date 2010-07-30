#!/usr/bin/env python
# pytorrent.py

from bencode import encode, decode
from hashlib import sha1
from urllib import urlencode, urlopen

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