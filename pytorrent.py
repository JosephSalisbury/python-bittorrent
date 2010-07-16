#!/usr/bin/env python
# pytorrent.py -- a torrent library for python

import bencode

f = open("test.torrent")
data = f.read()

d = bencode.decode(data)