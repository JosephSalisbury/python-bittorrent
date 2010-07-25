#!/usr/bin/env python
# pytorrent.py

import bencode

# Read the torrent file's contents
with open("test.torrent") as file:
	contents = file.read()

# Decode the torrent file's contents
data = bencode.decode(contents)

print data.keys()