#!/usr/bin/python

import cgi
import sqlite3

print "Content-Type: text/html\n"
print "<html><body>"
connection = sqlite3.connect('./database')
d = connection.cursor()

d.execute("CREATE TABLE stories (name TEXT, id INT, user TEXT, story TEXT, image TEXT, votes INT)")

for r in d:
	print r

connection.commit()
d.close()

print "Done!"
print "</body></html>"
