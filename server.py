from CGIHTTPServer import CGIHTTPRequestHandler as RH
from BaseHTTPServer import HTTPServer as HS

port = 8080

httpd = HS(('',port), RH)
httpd.serve_forever()
