#!/usr/bin/python

import cgi
import cgitb; cgitb.enable()
import sqlite3

print "Content-Type: text/html\n"
print "<html><body>"

print "<table border='1'><tr><th>Rank</th><th>Name</th><th>Author</th><th>Votes</th></tr>"

with sqlite3.connect('./database') as connection:
    d = connection.cursor()
    
    d.execute("SELECT * FROM stories ORDER BY votes DESC")
    

    rows = d.fetchall()

    for i in range(len(rows)):
        print "<tr>"
        print "<td>%d</td>" % (i+1)
        print "<td><a href='../stories/%d.html'>%s</a></td>" % (rows[i][1], rows[i][0])
        print "<td>%s</td>" % (rows[i][3])
        print "<td>%d</td>" % (rows[i][2])
        print "</tr>"
    
    d.close()

print "</table>"
print "</body></html>"
