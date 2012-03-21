#!/usr/bin/python

import cgi
import sqlite3

print "Content-Type: text/html"

form = cgi.FieldStorage()
print "<h2>Parameters</h2>"
print "<ul>"

connection = sqlite3.connect('./database')
d = connection.cursor()

d.execute('''create table test (txt text)''')
connection.commit()
d.close()

print "Done!"
