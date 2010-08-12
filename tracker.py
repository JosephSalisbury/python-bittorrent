# pytorrent-tracker.py
# A bittorrent tracker

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from bencode import encode
from pickle import dump, load
from socket import inet_aton
from SocketServer import ThreadingMixIn
from struct import pack
from urlparse import parse_qs

def read_torrent_db(torrent_db):
	try:
		with open(torrent_db, "r") as db:
			return load(db)
	except IOError:	# No file
		return {}

def write_torrent_db(torrent_db, data):
	with open(torrent_db, "w") as db:
		dump(data, db)

def decode_request(path):
	""" Return the decoded request string. """

	# Strip off the start characters
	if path[:1] == "?":
		path = path[1:]
	elif path[:2] == "/?":
		path = path[2:]

	return parse_qs(path)

def add_peer(torrents, info_hash, peer_id, ip, port):
	""" Add the peer to the torrent database. """

	# If we've heard of this, just add the peer
	if info_hash in torrents:
		# Only add the peer if they're not already in the database
		if (peer_id, ip, port) not in torrents[info_hash]:
			torrents[info_hash].append((peer_id, ip, port))
	# Otherwise, add the info_hash and the peer
	else:
		torrents[info_hash] = [(peer_id, ip, port)]

def make_compact_peer_list(peer_list):
	""" Return a compact peer string, given a list of peer details. """

	peer_string = ""
	for peer in peer_list:
		ip = inet_aton(peer[1])
		port = pack(">H", int(peer[2]))

		peer_string += (ip + port)

	return peer_string

def make_peer_list(peer_list):
	""" Return a peer list suitable for the client, given the peer list. """

	peers = []
	for peer in peer_list:
		p = {}
		p["peer id"] = peer[0]
		p["ip"] = peer[1]
		p["port"] = int(peer[2])

		peers.append(p)

	return peers

def peer_list(peer_list, compact):
	""" Depending on compact, dispatches to compact or expanded peer list functions. """

	if compact:
		return make_compact_peer_list(peer_list)
	else:
		return make_peer_list(peer_list)

class RequestHandler(BaseHTTPRequestHandler):
	def do_GET(s):
		# Decode the request
		package = decode_request(s.path)

		# Get the necessary info out of the request
		info_hash = package["info_hash"][0]
		compact = int(package["compact"][0])
		ip = s.client_address[0]
		port = package["port"][0]
		peer_id = package["peer_id"][0]

		add_peer(s.server.torrents, info_hash, peer_id, ip, port)

		# Generate a response
		response = {}
		response["interval"] = s.server.interval
		response["complete"] = 0
		response["incomplete"] = 0
		response["peers"] = peer_list(s.server.torrents[info_hash], compact)

		# Send off the response
		s.send_response(200)
		s.end_headers()
		s.wfile.write(encode(response))

		print "PACKAGE:", package
		print "DB:", s.server.torrents
		print "RESPONSE:", response
		print

# Means each HTTP request is handled in a seperate thread.
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	pass

class Tracker():
	def __init__(self, host = "", port = 9001, interval = 5, torrent_db = "tracker.db", inmemory = False):
		self.host = host
		self.port = port

		self.inmemory = inmemory

		self.server_class = ThreadedHTTPServer
		self.httpd = self.server_class((self.host, self.port), RequestHandler)

		self.server_class.interval = interval

		if not self.inmemory:	# If not in memory, load the db, otherwise it stays as {}
			self.torrent_db = torrent_db
			self.server_class.torrents = read_torrent_db(self.torrent_db)
		else:
			self.server_class.torrents = {}

	def run(self):
		try:
			self.httpd.serve_forever()
		except KeyboardInterrupt:
			pass

	def __del__(self):
		if not self.inmemory:	# If not in memory, persist the database
			write_torrent_db(self.torrent_db, self.server_class.torrents)
		self.httpd.server_close()

def main():
	t = Tracker(inmemory = True)
	t.run()

if __name__ == "__main__":
	main()