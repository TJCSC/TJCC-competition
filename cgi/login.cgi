#!/usr/bin/python

import cgi
import os, sys
import pickle
import sqlite3 as sql
from Cookie import SimpleCookie
import datetime


kookie, username = SimpleCookie(os.environ['HTTP_COOKIE']), ""
form = cgi.FieldStorage()
flag = True
if 'KOOKIE' in kookie:
    cookie = SimpleCookie(os.environ['HTTP_COOKIE'])['KOOKIE'].value
    username = cookie.split('_')[0]
    print 'Content-type: text/html\n'
    print "<html><body>"
    print 'Succesfully logged in as %s' % (username,)
    flag = False

elif 'username' in form and 'password' in form:
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
            password = session_obj[user]
            print 'Content-type: text/html\n'
            print "<html><body>"
            print 'Succesfully logged in as %s' % (user,)
            flag = False
        else:
            username=""
            print 'Content-type: text/html\n'
            print "<html><body>"
            print 'Invalid Login'
            connection.commit()
            d.close()
else:
    print 'Content-type: text/html\n'
    print "<html><body>"

if flag:
    print "<h1>Favorite Color Competition Login Page!</h1>"
    print "<form method='post'>"
    
    print "Username: <input type='text' name='username' value='' required/> <br />"
    print "Password: <input type='text' name='password' value='' required/> <br />"
    
    print "<br />"
    print "<input type='submit' value='submit form' />"
    print "</form>"

print "</body>"
print "</html>"
