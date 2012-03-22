#!/usr/bin/python

import cgi
import os, sys
from Cookie import SimpleCookie

print "Content-Type: text/html"
print
print "<html><body>"
print "<h1>Favorite Color Competition Login Page!</h1>"

print "<form method='post'>"

# standard single line text field
print "Username: <input type='text' name='username' value='' /> <br />"
print "Password: <input type='text' name='password' value='' /> <br />"

# text area

print "<br />"
print "<input type='submit' value='submit form' />"
print "</form>"

print "</body>"
print "</html>"
