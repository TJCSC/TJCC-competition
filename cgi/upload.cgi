#!/usr/bin/python

import cgi
import os, sys

print "Content-Type: text/html"
print
print "<html>"
print "<body>"

print "<h1>Favorite Color Competition Upload Page!</h1>"

print "<form method='post'>"

# standard single line text field
print "Color Name:"
print "<input type='text' name='color_name' value='' />"
print "<br />"

# text area
print "Story:<br />"
print "<textarea name='story' rows='10' cols='50'></textarea>"
print "<br />"

# file upload
print "Picture:"
print "<input type='file' name='picture'>"
print "<br />"

print "<br />"
print "<input type='submit' value='submit form' />"
print "</form>"

form = cgi.FieldStorage()
print "<h2>Parameters</h2>"
print "<ul>"
for field_name in form:
	field=form[field_name]
	print "<li>"
	print field.name
	print " = "
	print cgi.escape(repr(field.value))
	print "</li>"
print "</ul>"

print "</body>"
print "</html>"
