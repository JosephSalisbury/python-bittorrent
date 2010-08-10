# pytorrent-tracker.py
# A bittorrent tracker

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import parse_qs

HOST = ""
PORT = 9001

torrents = {}

class RequestHandler(BaseHTTPRequestHandler):
	def do_GET(s):
		package = parse_qs(s.path[1:])
		client_address = s.client_address

		info_hash = package["info_hash"][0]

		if not info_hash in torrents:
			print "NO HASH"
			torrents[info_hash] = [client_address]
		else:
			print "HAS HASH"
			torrents[info_hash].append(client_address)

		print "DB:", torrents


		s.send_response(200)
		s.end_headers()
		s.wfile.write("LOL")

class Tracker():
	def __init__(self):
		self.server_class = HTTPServer
		self.httpd = self.server_class((HOST, PORT), RequestHandler)

	def run(self):
		try:
			self.httpd.serve_forever()
		except KeyboardInterrupt:
			pass

		self.httpd.server_close()

if __name__ == "__main__":
	t = Tracker()
	t.run()