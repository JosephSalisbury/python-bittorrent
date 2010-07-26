#!/usr/bin/env python
# pytorrent.py

import bencode
import urllib
from hashlib import sha1

def read_torrent_file(torrent_file):
	# Read the torrent file's contents
	with open(torrent_file) as file:
		contents = file.read()

	# Decode the torrent file's contents
	return bencode.decode(contents)

def make_tracker_request(torrent):
	info = sha1(bencode.encode(torrent["info"])).hexdigest()

	data = {"info_hash" : info,
			"peer_id" : "ABCDEFGHIJKLMNOPQRST",
			"port" : 6969,
			"uploaded" : 0,
			"downloaded" : 0,
			"left" : None}
	data = urllib.urlencode(data)

	tracker_url = torrent["announce"]
	response = urllib.urlopen(tracker_url + "?" + data).read()

	return bencode.decode(response)

class Torrent():
	def __init__(self, torrent_file):
		self.data = read_torrent_file(torrent_file)

	def tracker_request(self):
		make_tracker_request(self.data)