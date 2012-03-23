import sqlite3 as sql
from subprocess import call

def main():

    if raw_input("Are you sure you want to do this? (y/n) ") != "y":
        exit()

    call("rm stories/*", shell=True)
    print 'Deleted html files'

    call("rm files/*", shell=True)
    print 'Deleted pictures'

    with sql.connect('./database') as connection:
        d = connection.cursor()
        
        d.execute("DELETE FROM stories")
    print 'Deleted database entries'

    print 'Done!'

if __name__ == '__main__': main()
