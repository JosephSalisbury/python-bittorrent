# pytorrent-tracker.py
# A bittorrent tracker

import BaseHTTPServer

HOST = ""
PORT = 9001

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_GET(s):
		print s.path

if __name__ == "__main__":
	server_class = BaseHTTPServer.HTTPServer
	httpd = server_class((HOST, PORT), RequestHandler)

	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass

	httpd.server_close()