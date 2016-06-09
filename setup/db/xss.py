import sqlite3
XSS_DB_NAME = "xss.db"
xss_db_path = None
def create(db_path, overwrite = False):
	global xss_db_path
	xss_db_path = db_path + XSS_DB_NAME
	print('Checking the COMMENTS table')
	conn = sqlite3.connect(xss_db_path)
	cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='COMMENTS';")
	if ((not cursor.fetchone()) or overwrite == True):
		conn.execute("DROP TABLE IF EXISTS COMMENTS")
		print("Creating the table COMMENTS")
		conn.execute('''CREATE TABLE IF NOT EXISTS COMMENTS
					(ID         INT PRIMARY KEY NOT NULL,
					NAME        TEXT            NOT NULL,
					COMMENT     TEXT            NOT NULL,
					DATECREATED INT             NOT NULL, 
					PARENT_ID   INT);''')
		conn.execute("INSERT INTO COMMENTS (ID, NAME, COMMENT, DATECREATED, PARENT_ID) \
					VALUES (1, 'Zaphod', 'Hello all you vulnerable peeps', '2016-01-01 12:00:00', Null)")
		conn.execute("INSERT INTO COMMENTS (ID, NAME, COMMENT, DATECREATED, PARENT_ID) \
					VALUES (2, 'The Guide', ' The best drink in existence is the Pan Galactic Gargle Blaster. It says that the effect of a Pan Galactic Gargle Blaster is like having your brains smashed out by a slice of lemon wrapped round a large gold brick.', '2016-01-01 12:20:00', Null)")
		conn.execute("INSERT INTO COMMENTS (ID, NAME, COMMENT, DATECREATED, PARENT_ID) \
					VALUES (3, 'Ford', 'I''ll take 6', '2016-01-01 12:21:00', 2)")
		conn.execute("INSERT INTO COMMENTS (ID, NAME, COMMENT, DATECREATED, PARENT_ID) \
					VALUES (4, 'Marvin', 'You would', '2016-01-01 12:22:00', 3)")
		conn.commit()
	conn.close
	print("Comments should be good to go")

def getComments():
	conn = sqlite3.connect(xss_db_path)
	cursor = conn.execute("SELECT ID, NAME, COMMENT, DATECREATED, PARENT_ID FROM COMMENTS ORDER BY ID")
	all_rows = cursor.fetchall()
	conn.close()
	return all_rows