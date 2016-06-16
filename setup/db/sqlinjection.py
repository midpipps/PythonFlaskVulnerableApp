import sqlite3
import logging

SQLI_DB_NAME = "simpleInjection.db"
sqli_db_path = None
#setup the tables and data for the simple sql injection page
def create(db_path, overwrite=False):
    global sqli_db_path
    sqli_db_path = db_path + SQLI_DB_NAME

    logging.info('Checking SimpleInjection')
    conn = sqlite3.connect(sqli_db_path)
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='SEARCH';")
    if ((not cursor.fetchone()) or overwrite == True):
        conn.execute("DROP TABLE IF EXISTS SEARCH")
        logging.info("Creating the table SEARCH")
        conn.execute('''CREATE TABLE IF NOT EXISTS SEARCH
                    (ID         INT PRIMARY KEY NOT NULL,
                    NAME        TEXT            NOT NULL,
                    PHONE       TEXT            NOT NULL,
                    DATECREATED INT             NOT NULL,
                    SECRET      TEXT            NOT NULL,
                    DISPLAY     INT             NOT NULL);''')
        logging.info("Adding in some data to  SEARCH")
        conn.execute("INSERT INTO SEARCH (ID, NAME, PHONE, DATECREATED, SECRET, DISPLAY) \
                    VALUES (1, 'Marvin1', '555-555-5555', '2016-01-01 12:00:00', 'Sureasecret', 1)")
        conn.execute("INSERT INTO SEARCH (ID, NAME, PHONE, DATECREATED, SECRET, DISPLAY) \
                    VALUES (2, 'Marvin2', '555-777-7777', '2015-07-23 12:00:00', 'Thisisnotassecretasyouthink', 1)")
        conn.execute("INSERT INTO SEARCH (ID, NAME, PHONE, DATECREATED, SECRET, DISPLAY) \
                    VALUES (3, 'Marvin3', '555-555-1212', '2016-11-12 12:00:00', 'OhNoesMySecrets', 1)")
        conn.execute("INSERT INTO SEARCH (ID, NAME, PHONE, DATECREATED, SECRET, DISPLAY) \
                    VALUES (4, 'Marvin4', '666-555-5555', '2015-08-04 12:00:00', 'Okifyoustealme', 0)")
        conn.execute("INSERT INTO SEARCH (ID, NAME, PHONE, DATECREATED, SECRET, DISPLAY) \
                    VALUES (5, 'Marvin5', '555-999-5555', '2018-09-20 12:00:00', 'NotSoSecret', 1)")
        conn.execute("INSERT INTO SEARCH (ID, NAME, PHONE, DATECREATED, SECRET, DISPLAY) \
                    VALUES (6, 'SecretUser', '424-242-4242', '2014-08-16 12:00:00', '44af595c-1b56-400d-951e-8407249c8446', 0)")
        conn.commit()
    conn.close()
    logging.info('SimpleInjection should be good to go')

def search(search):
    conn = sqlite3.connect(sqli_db_path)
    sql_string = "SELECT ID, NAME, PHONE, DATECREATED FROM SEARCH WHERE DISPLAY <> 0 AND NAME LIKE '%" + search + "%' ORDER BY ID"
    cursor = conn.execute("SELECT ID, NAME, PHONE, DATECREATED FROM SEARCH WHERE DISPLAY <> 0 AND NAME LIKE '%" + search + "%' ORDER BY ID")
    all_rows = (sql_string, cursor.fetchall())
    conn.close()
    return all_rows