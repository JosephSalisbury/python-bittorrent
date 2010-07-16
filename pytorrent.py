#!/usr/bin/env python
# pytorrent.py -- a torrent library for python

import sys
sys.path.append("bittorrent-bencode")
import bencode

f = open("test.torrent")
data = f.read()

d = decode(data)