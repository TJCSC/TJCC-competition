#!/usr/bin/env python

from CGIHTTPServer import CGIHTTPRequestHandler as RH
from BaseHTTPServer import HTTPServer as HS
import cgitb; cgitb.enable()    #enables error reporting

class Handler(RH):
    cgi_directories = ["/cgi"]

port = 8080

httpd = HS(('',port), Handler)
httpd.serve_forever()
