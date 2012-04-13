#!/usr/bin/python

import cgi
import os, sys
import pickle
import sqlite3 as sql
from Cookie import SimpleCookie
import datetime
import cgitb; cgitb.enable()

print "Content-Type: text/html"

kookie, username = SimpleCookie(os.environ['HTTP_COOKIE']), ""
form = cgi.FieldStorage()

success = False

if 'username' in form and 'password' in form:
    user, passwd = form.getvalue('username'), form.getvalue('password')
    with sql.connect('./database') as connection:
        d = connection.cursor()
        d.execute("SELECT * FROM users WHERE username='%s' AND password='%s' LIMIT 1" % (user, passwd)) 
        rows = d.fetchall()
        if len(rows) > 0:
            session_obj = {}
            session_obj[user] = [passwd]
            session_file = open(os.path.join('.sessions', user), 'wb')
            pickle.dump(session_obj, session_file, 1)
            session_file.close()
            cookie = SimpleCookie()
            cookie['KOOKIE'] = user+'_'+passwd
            cookie['KOOKIE']['path'] = '/'
            cookie['KOOKIE']['expires'] = \
                  (datetime.datetime.now() + datetime.timedelta(days=30)).strftime("%a, %d-%b-%Y %H:%M:%S PST")
            print cookie.output()
            success = True
            username = session_obj[user]
        else:
            username=""
            connection.commit()
            d.close()
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
"""
print "</head>"
print "<body>"
print """<!--Navbar -->
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
                        <li class='active'><a href='/cgi/login.cgi'><i class='icon-user icon-white'></i> %s</a></li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
""" % (SimpleCookie(os.environ['HTTP_COOKIE'])['KOOKIE'].value.split('_')[0] if 'KOOKIE' in kookie else user if success else 'Login')

print """<!--Header -->
    <div class='container'>
        <h1>FCC Login Page</h1>
        <p>Log in to your FCC account here.</p>
    </div>
""" 

if success:
    print "    <META HTTP-EQUIV='refresh' CONTENT='3;URL=/'>"
    print """<!--Info -->
    <div class='container'>
        <div class='alert alert-success'>
            <h1>Logged in successfully.</h1>
            <p>You will be automatically redirected in 3 seconds, or <a href='/'>click here</a>.</p>
        </div>
    </div>
"""
elif 'KOOKIE' in kookie:
    print """<!--Info -->
    <div class='container'>
        <div class='alert alert-error'>
            <h1>You are already logged in.</h1>
            <p><a href='/'>Click here to return to the front page.</a></p>
            <div class='row'>
                    <div class='span1'>
                        <p><a class='btn btn-danger btn-large' href='/cgi/logout.cgi'>Logout</a></p>
                    </div>
            </div>
        </div>
    </div>
"""
else:
    print """<!--Login form -->
    <div class='container'>
        <form class='well' method='post'>
            <fieldset>
            <label>Username:</label>
            <input type='text' name='username' value='' placeholder='Enter your username here' class='span3' required/> <br />

            <label>Password:</label>
            <input type='password' name='password' value='' placeholder='Enter your password here' class='span3' required/> <br />
            </fieldset>

            <button type='submit' class='btn btn-primary'>Submit</button>
            <p><br>Don't have an account? <a href='/cgi/register.cgi'>Register one here.</a></p>
         </form>
     </div>
"""

print """<!--Footer -->
    <div class="container">
        <footer class="footer">
            <hr>
            <p>&copy; Thomas Jefferson Computer Security Competition Club 2012</p>
        </footer>
    </div>
"""

print "</body>"
print "</html>"
