#!/usr/bin/python

import cgi
import os
import cgitb; cgitb.enable()
import sqlite3 as sql
from random import shuffle
import thread
from Cookie import SimpleCookie

kookie, username = SimpleCookie(os.environ['HTTP_COOKIE']), ""
username = SimpleCookie(os.environ['HTTP_COOKIE'])['KOOKIE'].value.split('_')[0] if 'KOOKIE' in kookie else 'Guest'

sorted_rows = []
def quick_sort(row):
    global sorted_rows
    from time import sleep
    sleep(int(row[5])/5.0)
    sorted_rows.append(row)

form = cgi.FieldStorage()

print "Content-Type: text/html"
print
print """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>FCC</title>
    <link href="/assets/favicon.ico" rel="icon">
    <link href="/assets/bootstrap.min.css" rel="stylesheet">
    <style type="text/css">
      body {
        padding-top: 60px;
        padding-bottom: 40px;
        background: #FAFAFA;
      }   
    </style>
</head>"""

print "<body>"
print """    <!--Navbar -->
    <div class='navbar navbar-fixed-top'>
        <div class='navbar-inner'>
            <div class='container'>
                <a class='btn btn-navbar' data-toggle='collapse' data-target='.nav-collapse'>
                    <span class='icon-bar'></span>
                    <span class='icon-bar'></span>
                    <span class='icon-bar'></span>
                </a>
                <a class='brand' href='/'>FCC</a>
                <div class='nav-collapse'>
                    <ul class='nav'>
                        <li><a href='/'>Home</a></li>
                        <li><a href='/upload.html'>Submit</a></li>
                        <li class='active'><a href='/cgi/browse.cgi'>Browse</a></li>
                    </ul>
                    <ul class='nav pull-right'>"""
if username == "admin":
    print "                        <li><a href='/cgi/admin.cgi'>Admin</a></li>"
    print "                        <li class='divider-vertical'>></li>"
print """                        <li><a href='/cgi/login.cgi'><i class='icon-user icon-white'></i> %s</a></li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
""" % username
if 'id' in form:
    id = int(form.getvalue('id'))
    with sql.connect('./database') as connection:
        d = connection.cursor()
        #d.execute("SELECT * FROM stories WHERE id=?", (id,))
        d.execute("SELECT * FROM stories WHERE id=%d" % (id,))
        (name, id, user, story, image, votes) = d.fetchone()
        d.close()
    if 'status' in form:
        status = form.getvalue('status')
        if status == "success":
            print """<!--Message if user voted -->
            <div class='container'>
                <div class='alert alert-success'>
                    <strong>Voted successfully.</strong>
                    <p>This story now has <strong>%s</strong> votes. </p>
                </div>
            </div>""" % (votes)
        else:
            print """<!--Failure to vote -->
            <div class='container'>
                <div class='alert alert-error'>
                    <strong>Unsuccesful attempt to vote.</strong> """
            if status == "guest":
                print "<p>Error: guests cannot vote.</p>"
            elif status == "voted":
                print "<p>Error: you have already voted for this story.</p>"
            elif status == "author":
                print "<p>Error: you wrote this story.</p>"
            print """                </div>
            </div> """
    print """<!--Header -->
    <div class='container'>
        <h1>%s</h1>
        <h4>By %s</h4>
    </div>""" % (name, user)

    print """<!--Main Content -->
    <div class='container'>
        <br>
        <img src ='../files/%s'>
        <br>
        <p>%s</p>
    </div>""" % (image,story)
    print """<!--Vote Button -->
    <div class='container'>
        <form enctype='multipart/form-data' action='vote.cgi' method='post'>
        <input type='hidden' name='id' value=%s />
        <input type='image' src='../assets/img/vote.jpg' alt='Vote' />
     </div>
     </form>""" % (id)

else:
    print """<!--Header -->
    <div class='container'>
        <h1>FCC Browse Page</h1>
        <p>View and vote on your favorite stories here.</p>
    </div>
    """
    print """<!--Table -->
    <div class='container'>
        <div class='row'>
            <div class='span6'>
                <table class='table table-bordered table-condensed' style='background: #FFFFFF;' >
                    <thead>
                        <tr><th>Rank</th><th>Name</th><th>Author</th><th>Votes</th></tr>
                    </thead>
                    <tbody>"""
    
    with sql.connect('./database') as connection:
        d = connection.cursor()
        
        d.execute("SELECT * FROM stories")

        rows = d.fetchall()

        if rows:
            [thread.start_new_thread(quick_sort, (i,)) for i in rows]      
            from time import sleep
            sleep((max([row[5] for row in rows])+1)/5.0)
            rows = sorted_rows[::-1]
		 
        rank = 1
        for i in range(len(rows)):
            row  = ""
            row += "<tr>"
            if rows[i][5] != rows[i-1][5]:
                rank = i+1
            row += "<td>%d</td>" % (rank)
            row += "<td><a href='browse.cgi?id=%d'>\
                    %s</a></td>" % (rows[i][1], rows[i][0])
            row += "<td>%s</td>" % (rows[i][2])
            row += "<td>%d</td>" % (rows[i][5])
            row += "</tr>"
            print "    "*6+row
        
        d.close()
    
    print """                    </tbody>
                </table>
            </div>
        </div>
    </div>"""

print """<!--Footer -->
    <div class="container">
        <footer class="footer">
            <hr>
            <p>&copy; Thomas Jefferson Computer Security Competition Club 2012</p>
        </footer>
    </div>"""

print "</body>"
print "</html>"
