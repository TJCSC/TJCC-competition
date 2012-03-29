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

    #d.execute('SELECT votes FROM stories WHERE id=?', (id,))
    d.execute('SELECT votes FROM stories WHERE id=%d' % (id,))
    votes = d.fetchone()[0]
    #d.execute('UPDATE stories SET votes=? WHERE id=?', (votes+1, id))
    d.execute('UPDATE stories SET votes=%d WHERE id=%d' % (votes+1, id))

    d.close()

print '<meta http-equiv="REFRESH" content="0;browse.cgi?id=%d">' % id

print "</body></html>"
