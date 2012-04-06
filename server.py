#!/usr/bin/env python

from CGIHTTPServer import CGIHTTPRequestHandler as RH
from BaseHTTPServer import HTTPServer as HS
import cgitb; cgitb.enable()    #enables error reporting
import os
import select
import sys


class Handler(RH):
    cgi_directories = ["/cgi"]

def init():
    if not os.path.exists("./files"):
        print "Creating ./files directory"
        os.makedirs("./files")

init()

port = 8080
httpd = HS(('',port), Handler)

running = True
while running:
    try:
        inready,outready,eready = select.select([httpd,sys.stdin],[],[])   # check for input from multiple sources
        for s in inready:
            if s == httpd: # input from HTTPServer
                httpd.handle_request()
            elif s == sys.stdin: # input from console
                line =  sys.stdin.readline().split()
                if line[0] in ["quit","exit","close","stop","halt"]:
                    running = False
                elif line[0] in ["delete","remove"]:
                    import deleteAllStories
                    if not deleteAllStories.main(): # re-create files/ to prevent errors
                        init()
                    
    except KeyboardInterrupt: # handle Ctrl-C properly
        break

print "Server shutting down."
httpd.socket.close()
