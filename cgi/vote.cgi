#!/usr/bin/env python
import cgi
import cgitb; cgitb.enable()
import sqlite3 as sql
import sys, os
from Cookie import SimpleCookie

print "Content-Type: text/html\n"
print "<html><body>"

form = cgi.FieldStorage()

id = int(form.getvalue('id'))

cookie = SimpleCookie(os.environ['HTTP_COOKIE'])
if 'KOOKIE' in cookie:
    username = cookie['KOOKIE'].value.split('_')[0]
    with sql.connect('./database') as connection:
        d = connection.cursor()
    
        #d.execute('SELECT votedFor FROM users WHERE username=?', (username,))
        d.execute('SELECT votedFor FROM users WHERE username="%s"' % (username,))
        votedFor = eval(d.fetchone()[0])
        d.execute('SELECT stories FROM users WHERE username="%s"' % (username,))
        stories = eval(d.fetchone()[0])
        if id in votedFor:
            print 'You have already voted for this story.<br />'
        elif id in stories:
            print 'You wrote this story no voting today.<br />'
        else:
            votedFor.append(id)
            #d.execute('UPDATE users SET votedFor=? WHERE username=?', (votedFor, username))
            d.execute('UPDATE users SET votedFor="%s" WHERE username="%s"' % (votedFor, username))
            #d.execute('SELECT votes FROM stories WHERE id=?', (id,))
            d.execute('SELECT votes FROM stories WHERE id=%d' % (id,))
            votes = d.fetchone()[0]
            #d.execute('UPDATE stories SET votes=? WHERE id=?', (votes+1, id))
            d.execute('UPDATE stories SET votes=%d WHERE id=%d' % (votes+1, id))
            print 'Current votes: %d<br />' % (votes+1,)
    
        connection.commit()
        d.close()
else:
    username = 'Guest'
    print "You must be logged in to vote.<br />"

print '<a href="browse.cgi?id=%d">Return</a>' % (id,)
print "</body></html>"
