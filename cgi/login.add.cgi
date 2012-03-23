#!/usr/bin/python

import cgi
import sqlite3

print "Content-Type: text/html\n"
print "<html><body>"
connection = sqlite3.connect('./database')
d = connection.cursor()

d.execute("INSERT INTO users VALUES (1,'herp','derp','Herpington','')")

for r in d:
	print r

connection.commit()
d.close()

print "Done!"
print "</body></html>"
