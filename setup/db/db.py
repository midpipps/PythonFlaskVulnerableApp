import setup.db.sqlinjection
import setup.db.xss
#This module will setup all the databases
#tables etc for the different pages.
DB_PATHS = "./dbs/"

def create(overwrite=False):
    setup.db.sqlinjection.create(DB_PATHS, overwrite)
    setup.db.xss.create(DB_PATHS, overwrite)