#!/usr/bin/env python
import cgi
import cgitb; cgitb.enable()
import sqlite3 as sql

print "Content-Type: text/html\n"
print "<html><body>"

form = cgi.FieldStorage()

id = int(form.getvalue('id'))

with sql.connect('./database') as connection:
    d = connection.cursor()

    d.execute('SELECT * FROM stories WHERE id=%d' % (id))
    row = list(d.fetchone())

    row[2] += 1

    d.execute('DELETE FROM stories WHERE id=%d' % (id))
    d.execute('INSERT INTO stories VALUES ("%s", %d, %d, "%s")' % tuple(row))

    d.close()

print '<meta http-equiv="REFRESH" content="0;../stories/%d.html">' % row[1]

print "</body></html>"
