#!/usr/bin/env python
import cgi, os
import cgitb; cgitb.enable()
import sqlite3 as sql
import random

try: # Windows needs stdio set for binary mode.
    import msvcrt
    msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
    msvcrt.setmode (1, os.O_BINARY) # stdout = 1
except ImportError:
    pass

form = cgi.FieldStorage()

# A nested FieldStorage instance holds the file
fileitem = form['picture']

# Test if the file was uploaded
if fileitem.filename:
   
   # strip leading path from file name to avoid directory traversal attacks
   fn = os.path.basename(fileitem.filename)
   open('files/' + fn, 'wb').write(fileitem.file.read())
   message = 'The file "' + fn + '" was uploaded successfully'
   
else:
   message = 'No file was uploaded'

id = random.randint(100, 999)

with sql.connect('./database') as connection:
    d = connection.cursor()
    
    d.execute('INSERT INTO stories VALUES (?, ?, ?, ?, ?, 0)', (form.getvalue('color_name'), id, 'kusoman', form.getvalue('story'), fn))
   
print """\
Content-Type: text/html\n
<html><body>
<meta http-equiv="REFRESH" content="0;browse.cgi?id=%d">
</body></html>
""" % (id,)
