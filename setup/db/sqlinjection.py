'''
helper class for the sql injection pages
'''
import sqlite3
import logging

SQLI_DB_NAME = "simpleInjection.db"
sqli_db_path = None
#setup the tables and data for the simple sql injection page
def create(db_path, overwrite=False):
    '''
    creates the db for sqlinjection and adds some data
    If overwrite is true it will drop the tables and recreate
    everything
    '''
    global sqli_db_path
    sqli_db_path = db_path + SQLI_DB_NAME

    logging.info('Checking SimpleInjection')
    conn = sqlite3.connect(sqli_db_path)
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='SEARCH';")
    if (not cursor.fetchone()) or overwrite is True:
        conn.execute("DROP TABLE IF EXISTS SEARCH")
        logging.info("Creating the table SEARCH")
        conn.execute('''CREATE TABLE IF NOT EXISTS SEARCH
                    (ID         INTEGER PRIMARY KEY NOT NULL,
                    NAME        TEXT            NOT NULL,
                    PHONE       TEXT            NOT NULL,
                    DATECREATED INT             NOT NULL,
                    SECRET      TEXT            NOT NULL,
                    DISPLAY     INT             NOT NULL);''')
        logging.info("Adding in some data to  SEARCH")
        search_insert('Marvin1', '555-555-5555', 'Sureasecret',
                      1, "'2016-01-01 12:00:00'", conn)
        search_insert('Marvin2', '555-777-7777', 'Thisisnotassecretasyouthink',
                      1, "'2015-07-23 12:00:00'", conn)
        search_insert('Marvin3', '555-555-1212', 'OhNoesMySecrets',
                      1, "'2016-11-12 12:00:00'", conn)
        search_insert('Marvin4', '666-555-5555', 'Okifyoustealme',
                      0, "'2015-08-04 12:00:00'", conn)
        search_insert('Marvin5', '555-999-5555', 'NotSoSecret',
                      1, "'2018-09-20 12:00:00'", conn)
        search_insert('SecretUser', '424-242-4242', '44af595c-1b56-400d-951e-8407249c8446',
                      0, "'2014-08-16 12:00:00'", conn)
        conn.commit()
    conn.close()
    logging.info('SimpleInjection should be good to go')

def search_insert(name, phone, secret, display=1, thedate="DATETIME('now')", conn=None):
    '''
    insert a new row to the search table
    '''
    sql_string = "INSERT INTO SEARCH (NAME, PHONE, DATECREATED, SECRET, DISPLAY) VALUES ('" \
                 + name + "', '" + phone + "', " +  thedate \
                 + ", '" + secret + "', " + str(display) + ")"
    if conn:
        conn.execute(sql_string)
        conn.commit()
    else:
        conn = sqlite3.connect(sqli_db_path)
        try:
            conn.execute(sql_string)
            conn.commit()
        finally:
            conn.close()

def search(searchstring):
    '''
    searches all the search rows for a name containing the search string
    '''
    all_rows = tuple()
    conn = sqlite3.connect(sqli_db_path)
    sql_string = "SELECT ID, NAME, PHONE, DATECREATED FROM SEARCH" \
                 + " WHERE DISPLAY <> 0 AND NAME LIKE '%" \
                 + searchstring + "%' ORDER BY ID"
    try:
        cursor = conn.execute(sql_string)
        all_rows = (sql_string, cursor.fetchall())
    finally:
        conn.close()
    return all_rows
