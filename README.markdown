python-bittorent
=========
python-bittorent is a BitTorrent library, written entirely in Python.
It aims to be simple, clean, and efficient.

Dependencies: (obviously) python, nose for testing.

bittorrent.py
------------
This module aims to make it *incredibly* simple to incorporate the BitTorrent protocol into your program.

To run a Bittorrent tracker from within your application:
    from bittorrent import Tracker
    tracker = Tracker()
    tracker.run()
and you're done!