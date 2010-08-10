# pytorrent-tracker.py
# A bittorrent tracker

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from pickle import dump, load
from urlparse import parse_qs

torrents = {}	# Global so RequestHandler can reach it

def read_torrent_db(torrent_db):
	try:
		with open(torrent_db, "r") as db:
			return load(db)
	except IOError:	# No file
		return {}

def write_torrent_db(torrent_db, data):
	with open(torrent_db, "w") as db:
		dump(data, db)

class Tracker():
	class RequestHandler(BaseHTTPRequestHandler):
		def do_GET(s):
			package = parse_qs(s.path[1:])
			client_address = s.client_address

			info_hash = package["info_hash"][0]

			if not info_hash in torrents:
				torrents[info_hash] = [client_address]
			else:
				torrents[info_hash].append(client_address)

			print "DB:", torrents

			s.send_response(200)
			s.end_headers()
			s.wfile.write("LOL")

	def __init__(self, host = "", port = 9001, torrent_db = "tracker.db"):
		self.host = host
		self.port = port

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
		write_torrent_db(self.torrent_db, torrents)
		self.httpd.server_close()

def main():
	t = Tracker()
	t.run()

if __name__ == "__main__":
	main()