#!/usr/bin/env python

import sqlite3 as sql
#from subprocess import call
from shutil import rmtree

def main():

    if raw_input("Are you sure you want to delete all stories and pictures? This cannot be undone! (y/n) ") != "y":
        return 1

#    call("rm files/*", shell=True)
    try:
        rmtree("./files/")
    except OSError:
        print 'Error: files/ did not exist'
    else:
        print 'Deleted pictures'

    with sql.connect('./database') as connection:
        d = connection.cursor()
        
        d.execute("DELETE FROM stories")
    print 'Deleted database entries'

    print 'Done!'

if __name__ == '__main__': main()
