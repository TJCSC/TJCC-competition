#!/usr/bin/env python
import cgi, os
import cgitb; cgitb.enable()
import sqlite3 as sql
import random
from Cookie import SimpleCookie

try: # Windows needs stdio set for binary mode.
    import msvcrt
    msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
    msvcrt.setmode (1, os.O_BINARY) # stdout = 1
except ImportError:
    pass

form = cgi.FieldStorage()

def fbuffer(f, chunk_size=10000):
    while True:
        chunk = f.read(chunk_size)
        if not chunk: break
        yield chunk

# A nested FieldStorage instance holds the file
fileitem = form['picture']

# Test if the file was uploaded
if fileitem.filename:
   
#   # strip leading path from file name to avoid directory traversal attacks
#   fn = os.path.basename(fileitem.filename)
    fn = fileitem.filename
    with open('files/' + fn, 'wb', 10000) as f:
        for chunk in fbuffer(fileitem.file):
            f.write(chunk)
#   message = 'The file "' + fn + '" was uploaded successfully'
else:
    message = 'No file was uploaded'

id = random.randint(100, 999)

cookie = SimpleCookie(os.environ['HTTP_COOKIE'])
if 'KOOKIE' in cookie:
    username = cookie['KOOKIE'].value.split('|')[0]
else:
    username = 'guest'

with sql.connect('./database') as connection:
    d = connection.cursor()
    
    d.execute('INSERT INTO stories VALUES (?, ?, ?, ?, ?, 0)', (form.getvalue('color_name'), id, username, form.getvalue('story'), fn))
#    d.execute('INSERT INTO stories VALUES ("%s", "%d", "%s", "%s", "%s", 0)' % (form.getvalue('color_name'), id, username, form.getvalue('story'), fn))
   
print """\
Content-Type: text/html\n
<html><body>
<meta http-equiv="REFRESH" content="0;browse.cgi?id=%d">
</body></html>
""" % (id,)
