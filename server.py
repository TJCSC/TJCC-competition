#!/usr/bin/env python

from CGIHTTPServer import CGIHTTPRequestHandler as RH
from BaseHTTPServer import HTTPServer as HS
import cgitb; cgitb.enable()    #enables error reporting
import os

class Handler(RH):
    cgi_directories = ["/cgi"]

if not os.path.exists("./files"):
    print "Creating ./files directory"
    os.makedirs("./files")

port = 8080

httpd = HS(('',port), Handler)
httpd.serve_forever()
