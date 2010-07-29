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

	def get_announce_url(self):
		return self.data["announce"]

	def get_info(self):
		return self.data["info"]

	def get_tracker_response(self):
		if not self.tracker_response:
			self.make_tracker_request()

		return self.tracker_response

	def make_tracker_request(self):
		# Hash the info file, for the tracker
		info = self.get_info()
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
		tracker_url = self.get_announce_url()
		response = urlopen(tracker_url + "?" + payload).read()

		self.tracker_response = decode(response)