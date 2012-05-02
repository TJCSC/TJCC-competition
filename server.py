#!/usr/bin/env python

from CGIHTTPServer import CGIHTTPRequestHandler as RH
from BaseHTTPServer import HTTPServer as HS
import cgitb; cgitb.enable()    #enables error reporting
import os

class Handler(RH):
    cgi_directories = ["/cgi"]

def init():
    if not os.path.exists("./files"):
        print "Creating ./files directory"
        os.makedirs("./files")
    if not os.path.exists("./.sessions"):
        print "Creating ./.sessions directory"
        os.makedirs("./.sessions")

init()

port = 8080
httpd = HS(('',port), Handler)

while True:
    try:
        httpd.handle_request()
    except KeyboardInterrupt: # handle Ctrl-C properly
        break

print "Server shutting down."
httpd.socket.close()
