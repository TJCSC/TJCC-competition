#!/usr/bin/python

import cgi
import os
import cgitb; cgitb.enable()
import sqlite3 as sql
from random import shuffle
import thread
from Cookie import SimpleCookie

kookie, username = SimpleCookie(os.environ['HTTP_COOKIE']), ""


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
                        <li><a href='/cgi/browse.cgi'>Browse</a></li>
                    </ul>
                    <ul class='nav pull-right'>
                        <li class='active'><a href='/cgi/admin.cgi'>Admin</a></li>
                        <li class='divider-vertical'></li>
                        <li><a href='/cgi/login.cgi'><i class='icon-user icon-white'></i> %s</a></li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
""" % (SimpleCookie(os.environ['HTTP_COOKIE'])['KOOKIE'].value.split('_')[0] if 'KOOKIE' in kookie else 'Login')
form = cgi.FieldStorage()
print form


if not 'KOOKIE' in kookie or not kookie['KOOKIE'].value.split('_')[0] == 'admin':
    print "    <META HTTP-EQUIV='refresh' CONTENT='5;URL=/'>"
    print """<!--Info -->
    <div class='container'>
        <div class='alert alert-error'>
            <h1>You must be logged in as admin to view this page.</h1>
            <p>You will be automatically redirected in 5 seconds, or <a href="/">click here</a>.</p>
        </div>
    </div>
"""
elif 'id' in form:
    id = int(form.getvalue('id'))
    with sql.connect('./database') as connection:
        d = connection.cursor()
        #d.execute("SELECT * FROM stories WHERE id=?", (id,))
        d.execute("SELECT * FROM stories WHERE id=%d" % (id,))
        (name, id, user, story, image, votes) = d.fetchone()
        d.close()
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
        <h1>FCC Admin Panel</h1>
        <p>Perform admininistrative actions here.</p>
    </div>
    """
    print """<!--Table -->
    <div class='container'>
        <div class='row'>
            <div class='span6'>
<form method='post'> 
                <table class='table table-bordered table-condensed' style='background: #FFFFFF;' >
                    <thead>
                        <tr><th>Rank</th><th>Name</th><th>Author</th><th>Votes</th><th>Delete?</th></tr>
                    </thead>
                    <tbody>
                        <fieldset>"""
    
    with sql.connect('./database') as connection:
        d = connection.cursor()
        
        d.execute("SELECT * FROM stories")

        rows = d.fetchall()

        if rows:
            list.sort(rows)
            rows = rows[::-1]
		 
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
            #row += "<td><a href='/cgi/admin.cgi?did=%d' class='btn btn-mini btn-danger'>Delete</a></form></td>" % (rows[i][1])
            row += "<td><input type='checkbox' name='B%d' value='A%d' /></td>" % (rows[i][1],rows[i][1])
            row += "</tr>"
            print "    "*6+row
        
        d.close()
    
    print """                   </fieldset> 
                            </tbody>
                </table>
                            <button type='submit' class='btn btn-danger'>Delete selected stories</button>
                                </form>
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
