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
	info = sha1( bencode.encode( torrent["info"] )).digest()

	data = {"info_hash" : info}
	data = urllib.urlencode(data)

	tracker_url = torrent["announce"]
	response = urllib.urlopen(tracker_url + "?" + data).read()

	print response

def r():
	t = read_torrent_file("test.torrent")
	make_tracker_request(t)
