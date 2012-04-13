#!/usr/bin/python

import cgi
import sqlite3 as sql

print "Content-Type: text/html\n"
print "<html><body>"
print "<h1>Sign Up For Neopets!</h1>"
print "<form method='post'>"
print

form = cgi.FieldStorage()

if 'username' in form and 'password' in form and 'verify' in form:
    username = form.getvalue('username')
    password = form.getvalue('password')
    verify = form.getvalue('verify')
    if verify != password:
        print "Username: <input type='text' name='username' value='%s' required/><br />" % (username,)
        print 'Passwords do not match <br />'
    else:
        with sql.connect('./database') as connection:
            d = connection.cursor()
            
            d.execute('SELECT * FROM users WHERE username="%s" LIMIT 1' % (username,))
            if len(d.fetchall()) > 0:
                print 'Username is already taken <br />'
                print "Username: <input type='text' name='username' value='' required/><br />"
            else:
                d.execute('INSERT INTO users VALUES ("%s", "%s", "[]", "[]")' % (username, password))
        
                connection.commit()
                d.close()
                print '<meta http-equiv="REFRESH" content="0;login.cgi?username=%s&password=%s">' % (username, password)

else:
    print "Username: <input type='text' name='username' value='' required/> <br />"
print "Password: <input type='text' name='password' value='' required/> <br />"
print "Verify Password: <input type='text' name='verify' value='' required/> <br />"
print "<br />"
print "<input type='submit' value='submit form' />"
print "</form>"
print "</body></html>"
