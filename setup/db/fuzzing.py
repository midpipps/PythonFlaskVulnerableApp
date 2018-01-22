import sqlite3
import logging

XSS_DB_NAME = "fuzzing.db"
xss_db_path = None
def create(db_path, overwrite = False):
    global xss_db_path
    xss_db_path = db_path + XSS_DB_NAME
    logging.info('Checking the fuzzing table')
    conn = sqlite3.connect(xss_db_path)
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='FUZZING';")
    if ((not cursor.fetchone()) or overwrite == True):
        conn.execute("DROP TABLE IF EXISTS FUZZING")
        logging.info("Creating the table FUZZING")
        conn.execute('''CREATE TABLE IF NOT EXISTS FUZZING
                    (ID         INTEGER PRIMARY KEY NOT NULL,
                    NAME        TEXT            NOT NULL,
                    DATA        TEXT            NOT NULL);''')
        conn.execute("INSERT INTO FUZZING (ID, NAME, DATA) \
                    VALUES (1, 'Guest', 'Your account has no data here you are just a guest')")
        conn.execute("INSERT INTO FUZZING (ID, NAME, DATA) \
                    VALUES (2, 'Zaphod', 'The presidents account has no real power')")
        conn.execute("INSERT INTO FUZZING (ID, NAME, DATA) \
                    VALUES (3, 'Ford', 'Who even gave this guy an account')")
        conn.execute("INSERT INTO FUZZING (ID, NAME, DATA) \
                    VALUES (10, 'The Guide', 'The answer to life the universe and everything is in this password TkRJPQ==')")
        conn.execute("INSERT INTO FUZZING (ID, NAME, DATA) \
                    VALUES (4, 'Arthur', 'Seriously you gave the sandwich maker an account')")
        conn.execute("INSERT INTO FUZZING (ID, NAME, DATA) \
                    VALUES (12, 'Trillian', 'Maybe the only trustworthy human ever')")
        conn.commit()
    conn.close
    logging.info("FUZZING should be good to go")

def getFuzzing(id):
    conn = sqlite3.connect(xss_db_path)
    cursor = conn.execute("SELECT ID, NAME, DATA FROM FUZZING WHERE ID=?", (id,))
    all_rows = cursor.fetchone()
    conn.close()
    return all_rows
