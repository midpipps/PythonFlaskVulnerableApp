#This module will setup all the databases
#tables etc for the different pages.
import sqlite3

def simpleInjection(overwrite=False):
	print('Checking SimpleInjection')
	conn = sqlite3.connect('simpleInjection.db')
	cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='SEARCH';")
	if ((not cursor.fetchone()) or overwrite == True):
		conn.execute("DROP TABLE IF EXISTS SEARCH")
		print("Creating the table SEARCH")
		conn.execute('''CREATE TABLE IF NOT EXISTS SEARCH
					(ID         INT PRIMARY KEY NOT NULL,
					NAME        TEXT            NOT NULL,
					COMMENT     TEXT            NOT NULL,
					DATECREATED INT             NOT NULL,
					SECRET      TEXT            NOT NULL,
					DISPLAY     INT             NOT NULL);''')
		print("Adding in some data to  SEARCH")
		conn.execute("INSERT INTO SEARCH (ID, NAME, COMMENT, DATECREATED, SECRET, DISPLAY) \
					VALUES (1, 'Marvin1', 'You can blame the Sirius Cybernetics Corporation for making androids with GPP', '2016-01-01 12:00:00', 'Sureasecret', 1)")
		conn.execute("INSERT INTO SEARCH (ID, NAME, COMMENT, DATECREATED, SECRET, DISPLAY) \
					VALUES (2, 'Marvin2', 'Don''t see what the big deal is... Vogons are some of the worst shots in the galaxy...', '2015-07-23 12:00:00', 'Thisisnotassecretasyouthink', 1)")
		conn.execute("INSERT INTO SEARCH (ID, NAME, COMMENT, DATECREATED, SECRET, DISPLAY) \
					VALUES (3, 'Marvin3', 'Not that anyone cares what I say, but the restaurant is at the *other* end of the Universe.', '2016-11-12 12:00:00', 'OhNoesMySecrets', 1)")
		conn.execute("INSERT INTO SEARCH (ID, NAME, COMMENT, DATECREATED, SECRET, DISPLAY) \
					VALUES (4, 'Marvin4', 'I''ve calculated your chance of survival, but I don''t think you''ll like it.', '2015-08-04 12:00:00', 'Okifyoustealme', 1)")
		conn.execute("INSERT INTO SEARCH (ID, NAME, COMMENT, DATECREATED, SECRET, DISPLAY) \
					VALUES (5, 'Marvin5', 'You think you''ve got problems. What are you supposed to do if you are a manically depressed robot? No, don''t even bother answering. I''m 50,000 times more intelligent than you and even I don''t know the answer.', '2018-09-20 12:00:00', 'NotSoSecret', 1)")
		conn.execute("INSERT INTO SEARCH (ID, NAME, COMMENT, DATECREATED, SECRET, DISPLAY) \
					VALUES (6, 'SecretUser', 'HAHAHA You can''t see me', '2014-08-16 12:00:00', '44af595c-1b56-400d-951e-8407249c8446', 0)")
		conn.commit()
	conn.close()
	print('SimpleInjection should be good to go')

def run(overwrite=False):
	simpleInjection(overwrite)