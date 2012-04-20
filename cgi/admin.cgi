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

if 'did' in form:
    idlist = (form.getvalue('did'))
    if type(idlist) == str:
        idlist = [idlist]
    for id in idlist:
        id = int(id)

        with sql.connect('./database') as connection:
            d = connection.cursor()
            d.execute("DELETE FROM stories WHERE id=%d" % (id,))
            d.close()

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
                        <tbody>"""
    
    with sql.connect('./database') as connection:
        d = connection.cursor()
        
        d.execute("SELECT * FROM stories")

        rows = d.fetchall()

        if rows:
            list.sort(rows)
            rows = rows[::-1]
		 
        rank = 1
        for i in range(len(rows)):
            row  = "    "
            row += "<tr>"
            if rows[i][5] != rows[i-1][5]:
                rank = i+1
            row += "<td>%d</td>" % (rank)
            row += "<td><a href='browse.cgi?id=%d'>\
                    %s</a></td>" % (rows[i][1], rows[i][0])
            row += "<td>%s</td>" % (rows[i][2])
            row += "<td>%d</td>" % (rows[i][5])
            row += "<td><input type='checkbox' name='did' value='%d' /></td>" % (rows[i][1])
            row += "</tr>"
            print "    "*6+row
        
        d.close()
    
    print """                        </tbody>
                        </table>
                    <button type='submit' class='btn btn-danger pull-right'>Delete selected stories</button>
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
