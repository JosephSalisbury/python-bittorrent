# pytorrent-tracker.py
# A bittorrent tracker

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from bencode import encode
from pickle import dump, load
from socket import inet_aton
from struct import pack
from urlparse import parse_qs

torrents = {}	# Global so RequestHandler can reach it
INTERVAL = 1800

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

class Tracker():
	class RequestHandler(BaseHTTPRequestHandler):
		def do_GET(s):
			# Decode the request
			package = decode_request(s.path)
			print "PACKAGE:", package

			# Get the necessary info out of the request
			info_hash = package["info_hash"][0]
			compact = int(package["compact"][0])
			ip = s.client_address[0]
			port = package["port"][0]
			peer_id = package["peer_id"][0]

			# If we've heard of this, add the peer, else add the hash and the peer
			if info_hash in torrents:
				torrents[info_hash].append((peer_id, ip, port))
			else:
				torrents[info_hash] = [(peer_id, ip, port)]

			print "DB:", torrents

			# Generate a response
			response = {}
			response["interval"] = INTERVAL
			response["complete"] = 0
			response["incomplete"] = 0
			response["peers"] = peer_list(torrents[info_hash], compact)

			print "RESPONSE:", response

			# Send off the response
			s.send_response(200)
			s.end_headers()
			s.wfile.write(encode(response))

	def __init__(self, host = "", port = 9001, interval = 1800, torrent_db = "tracker.db", inmemory = False):
		self.host = host
		self.port = port

		self.inmemory = inmemory

		if not self.inmemory:	# If not in memory, load the db, otherwise it stays as {}
			self.torrent_db = torrent_db
			global torrents
			torrents = read_torrent_db(self.torrent_db)

		self.server_class = HTTPServer
		self.httpd = self.server_class((self.host, self.port), self.RequestHandler)

	def run(self):
		try:
			self.httpd.serve_forever()
		except KeyboardInterrupt:
			pass

	def __del__(self):
		if not self.inmemory:	# If not in memory, persist the database
			write_torrent_db(self.torrent_db, torrents)
		self.httpd.server_close()

def main():
	t = Tracker(inmemory = True)
	t.run()

if __name__ == "__main__":
	main()