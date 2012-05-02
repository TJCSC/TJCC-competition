#!/usr/bin/python

import cgi
import sqlite3 as sql

import os
from Cookie import SimpleCookie
import cgitb; cgitb.enable()


kookie = SimpleCookie(os.environ['HTTP_COOKIE'])
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
                        <li><a href='/cgi/browse.py'>Browse</a></li>
                    </ul>
                    <ul class='nav pull-right'>
                        <li class='active'><a href='/cgi/login.py'><i class='icon-user icon-white'></i> %s</a></li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
""" % (SimpleCookie(os.environ['HTTP_COOKIE'])['KOOKIE'].value.split('_')[0] if 'KOOKIE' in kookie else 'Login')


print """<!--Header -->
    <div class='container'>
        <h1>FCC account creation page</h1>
    </div>
"""

form = cgi.FieldStorage()

success = False
verified = True
availible = True
if 'username' in form and 'password' in form and 'verify' in form:
    username = form.getvalue('username')
    password = form.getvalue('password')
    verify = form.getvalue('verify')
    if verify != password:
        verified = False
    else:
        with sql.connect('./database') as connection:
            d = connection.cursor()
            
            d.execute('SELECT * FROM users WHERE username="%s" LIMIT 1' % (username,))
            if len(d.fetchall()) > 0:
                availible = False
            else:
                d.execute('INSERT INTO users VALUES ("%s", "%s", "[]", "[]")' % (username, password))
        
                connection.commit()
                d.close()
                success = True

if success:
    print "		<meta http-equiv='REFRESH' content='0;login.py?username=%s&password=%s'>" % (username, password)
    print """<!--Info -->
    <div class='container'>
        <div class='alert alert-success'>
            <h1>Account created successfully.</h1>
            <p>You will be automatically logged in, or <a href="/cgi/login.py">click here to log in manually</a>.</p>
        </div>
    </div>
"""
elif 'KOOKIE' in kookie:
	cookie = SimpleCookie(os.environ['HTTP_COOKIE'])['KOOKIE'].value
	username = cookie.split("_")[0]
	password = cookie.split("_")[1]

	print "    <META HTTP-EQUIV='refresh' CONTENT='5;URL=/'>"
	print """<!--Info -->
    <div class='container'>
        <div class='alert alert-error'>
            <h1>Already logged in.</h1>
            <p>You will be automatically redirected in 5 seconds, or <a href="/">click here</a>.</p>
        </div>
    </div>
"""
else:
    print """<!--Registration form -->
	<div class='container'>
		<form class='well' method='post'>
			<fieldset>"""

    print """
			<label>Username:</label>
			<input type='text' name='username' value='' placeholder='Enter your username here' class='span3' required/>"""
    if not availible:
        print "			<span class='help-inline'>Username is already taken</span>"

    print """
			<label>Password:</label>
			<input type='password' name='password' value='' placeholder='Enter your password here' class='span3' required/>"""
    if not verified:
            print "			<span class='help-inline'>Passwords do not match</span>"
    print """
			<label>Verify Password:</label>
			<input type='password' name='verify' value='' placeholder='Enter your password again' class='span3' required/>"""

    print """         
			</fieldset>
			<button type='submit' class='btn btn-primary'>Register</button>
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
