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

if form.has_key('picture'):
    pic = form['picture']
    print pic
    print dir(pic)
    print pic.type
    if pic.file: 
        with file(os.path.join('/pix', pic.filename), 'wb') as fout:
            while 1:
                chunk = pic.file.read(100000)
                if not chunk: break
                fout.write(chunk)
    else:
        print "Invalid file"
else:
    print "No picture chosen<br />"


print "</body>"
print "</html>"
