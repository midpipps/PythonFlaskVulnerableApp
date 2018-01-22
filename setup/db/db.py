'''
Simple middle layer that just creates all the dbs
and any other maintenance on the dbs
'''
import setup.db.sqlinjection
import setup.db.xss
import setup.db.fuzzing
#This module will setup all the databases
#tables etc for the different pages.
DB_PATHS = "./dbs/"

def create(overwrite=False):
    '''
    Call the create method on the db classes
    if overwrite true then they should drop and
    completely recreate the db's
    '''
    setup.db.sqlinjection.create(DB_PATHS, overwrite)
    setup.db.xss.create(DB_PATHS, overwrite)
    setup.db.fuzzing.create(DB_PATHS, overwrite)
