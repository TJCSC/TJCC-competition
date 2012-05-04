#!/usr/bin/python

import cgi
import os, sys
import pickle
import sqlite3 as sql
from Cookie import SimpleCookie
import datetime
import cgitb; cgitb.enable()

print "Content-Type: text/html"

kookie, username = SimpleCookie(os.environ['HTTP_COOKIE']), ""
form = cgi.FieldStorage()

success = False

if 'KOOKIE' in kookie:
    user = kookie['KOOKIE'].value.split('_')[0]
    os.remove(os.path.join('.sessions', user))
    cookie = SimpleCookie()
    cookie['KOOKIE'] = ''
    cookie['KOOKIE']['path'] = '/'
    cookie['KOOKIE']['expires'] = \
          (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%a, %d-%b-%Y %H:%M:%S PST")
    print cookie.output()
    success = True
print
print """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>FCC</title>
    <link href="/assets/favicon.ico" rel="icon">
    <link href="/assets/bootstrap.min.css" rel="stylesheet">
    <style type="text/css">
      body {
        padding-top: 60px;
        padding-bottom: 40px;
        background: #FAFAFA;
      }   
    </style>
"""
print "</head>"
print "<body>"
print """<!--Navbar -->
    <div class='navbar navbar-fixed-top'>
        <div class='navbar-inner'>
            <div class='container'>
                <a class='brand' href='/'>FCC</a>
                <ul class='nav'>
                    <li><a href='/'>Home</a></li>
                    <li><a href='/upload.html'>Submit</a></li>
                    <li><a href='/cgi/browse.py'>Browse</a></li>
                </ul>
                <ul class='nav pull-right'>
                    <li><a href='/cgi/login.py'><i class='icon-user icon-white'></i> Login</a></li>
                </ul>
            </div>
        </div>
    </div>
""" 

print """<!--Header -->
    <div class='container'>
        <h1>FCC Logout Page</h1>
        <p>You will be logged out of your FCC account here.</p>
    </div>
""" 

if success:
    print "    <META HTTP-EQUIV='refresh' CONTENT='3;URL=/'>"
    print """<!--Info -->
    <div class='container'>
        <div class='alert alert-success'>
            <h1>Logged out successfully.</h1>
            <p>You will be automatically redirected in 3 seconds, or <a href="/">click here</a>.</p>
        </div>
    </div>
"""
else:
    print "    <META HTTP-EQUIV='refresh' CONTENT='3;URL=/'>"
    print """<!--Info -->
    <div class='container'>
        <div class='alert alert-error'>
            <h1>You were not logged in.</h1>
            <p>You will be automatically redirected in 3 seconds, or <a href="/">click here</a>.</p>
        </div>
    </div>
"""

print """<!--Footer -->
    <div class="container">
        <footer class="footer">
            <hr>
            <p>&copy; Thomas Jefferson Computer Security Competition Club 2012</p>
        </footer>
    </div>
"""

print "</body>"
print "</html>"
