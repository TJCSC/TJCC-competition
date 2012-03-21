#!/usr/bin/python

import cgi
import sqlite3

print "Content-Type: text/html"
print "<html><body>"
connection = sqlite3.connect('./database')
d = connection.cursor()

d.execute('select * from users')

for r in d:
	print r

connection.commit()
d.close()

print "Done!"
print "</body></html>"
