import sqlite3
import logging

XSS_DB_NAME = "xss.db"
xss_db_path = None
def create(db_path, overwrite = False):
    global xss_db_path
    xss_db_path = db_path + XSS_DB_NAME
    logging.info('Checking the COMMENTS table')
    conn = sqlite3.connect(xss_db_path)
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='COMMENTS';")
    if ((not cursor.fetchone()) or overwrite == True):
        conn.execute("DROP TABLE IF EXISTS COMMENTS")
        logging.info("Creating the table COMMENTS")
        conn.execute('''CREATE TABLE IF NOT EXISTS COMMENTS
                    (ID         INTEGER PRIMARY KEY NOT NULL,
                    NAME        TEXT            NOT NULL,
                    COMMENT     TEXT            NOT NULL,
                    DATECREATED INT             NOT NULL, 
                    PARENT_ID   INT             NOT NULL);''')
        addComment('Zaphod', 'Hello all you vulnerable peeps', 0, "'2016-01-01 12:00:00'", conn)
        addComment('The Guide', ' The best drink in existence is the Pan Galactic Gargle Blaster. It says that the effect of a Pan Galactic Gargle Blaster is like having your brains smashed out by a slice of lemon wrapped round a large gold brick.', 0, "'2016-01-01 12:20:00'", conn)
        addComment('Ford', 'I''ll take 6', 2, "'2016-01-01 12:21:00'", conn)
        addComment('Marvin', 'You would', 3, "'2016-01-01 12:22:00'", conn)
    conn.close
    logging.info("Comments should be good to go")

def getComments():
    conn = sqlite3.connect(xss_db_path)
    cursor = conn.execute("SELECT ID, NAME, COMMENT, DATECREATED, PARENT_ID FROM COMMENTS ORDER BY ID")
    all_rows = cursor.fetchall()
    conn.close()
    return all_rows

def addComment(name, comment, parentID, dt = "DATETIME('now')", conn = None):
    sqlstring = "INSERT INTO COMMENTS (NAME, COMMENT, DATECREATED, PARENT_ID) VALUES (?, ?, DATETIME('now'), ?)"
    if (conn):
        conn.execute(sqlstring, (name, comment, parentID))
        conn.commit()
    else:
        conn = sqlite3.connect(xss_db_path)
        conn.execute(sqlstring, (name, comment, parentID))
        conn.commit()
        conn.close