#!/usr/bin/python

import cgi
import cgitb; cgitb.enable()
import sqlite3 as sql

form = cgi.FieldStorage()

print "Content-Type: text/html\n"
print "<html><body>"

if 'id' in form:
    id = int(form.getvalue('id'))
    with sql.connect('./database') as connection:
        d = connection.cursor()
        d.execute("SELECT * FROM stories WHERE id=?", (id,))
        (name, id, user, story, image, votes) = d.fetchone()
        d.close()
    print "<a name='top' />"
    print "<h3>%s by %s</h3>" % (name, user)
    print "<p>%s</p>" % (story)
    print "<img src='../files/%s'><br>" % (image)
    print "<form enctype='multipart/form-data' action='vote.cgi' method='post'>"
    print "<input type='hidden' name='id' value=%s />" % (id)
    print "<input type='image' src='http://blogs.psychcentral.com/depression/files/2011/08/vote.jpg' alt='Vote' width='48' height='48' />"
    print "</form>"
    print "[<a href='../index.html'>home</a>]"
    print "[<a href='../cgi/browse.cgi'>browse</a>]"
    print "[<a href='#top'>top</a>]"
else:
    print "[<a name='top' href='../index.html'>home</a>]<br><br>"
    
    print "<table border='1'><tr><th>Rank</th><th>Name</th><th>Author</th><th>Votes</th></tr>"
    
    with sql.connect('./database') as connection:
        d = connection.cursor()
        
        d.execute("SELECT * FROM stories ORDER BY votes DESC")
        
    
        rows = d.fetchall()
		 
        rank = 1
        for i in range(len(rows)):
            print "<tr>"
            if rows[i][5] != rows[i-1][5]:
                rank = i+1
            print "<td>%d</td>" % (rank)
            print "<td><a href='browse.cgi?id=%d'>\
                    %s</a></td>" % (rows[i][1], rows[i][0])
            print "<td>%s</td>" % (rows[i][2])
            print "<td>%d</td>" % (rows[i][5])
            print "</tr>"
        
        d.close()
    
    print "</table><br>"
    print "[<a href='#top'>top</a>]"
print "</body></html>"
