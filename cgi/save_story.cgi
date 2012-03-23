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
    
    d.execute('INSERT INTO stories VALUES ("%s", %d, 0, "%s")' % (form.getvalue('color_name'), id, 'kusoman'))


with open('stories/' + str(id) + '.html', 'w') as storyFile:
    storyFile.write('''<html><body>
    <a name='top' />
    <h3>%s by %s</h3>
    <p>%s</p>
    <img src='../files/%s'><br>
    <form enctype='multipart/form-data' action='../cgi/vote.cgi' method='post'>
    <input type='hidden' name='id' value=%s />
    <input type='image' src='http://blogs.psychcentral.com/depression/files/2011/08/vote.jpg' alt='Vote' width='48' height='48' />
    </form>
    [<a href='../index.html'>home</a>]
    [<a href='../cgi/browse.cgi'>browse</a>]
    [<a href='#top'>top</a>]
    </body></html>'''
    % (form.getvalue('color_name'), 'kusoman', form.getvalue('story'), fn, str(id)))

message = str(id) + '.html'
   
print """\
Content-Type: text/html\n
<html><body>
<meta http-equiv="REFRESH" content="0;../stories/%d.html">
</body></html>
""" % (id,)
