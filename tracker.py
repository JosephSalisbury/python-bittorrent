# pytorrent-tracker.py
# A bittorrent tracker

import BaseHTTPServer
from urlparse import parse_qs

HOST = ""
PORT = 9001

torrents = {}

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
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

if __name__ == "__main__":
	server_class = BaseHTTPServer.HTTPServer
	httpd = server_class((HOST, PORT), RequestHandler)

	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass

	httpd.server_close()