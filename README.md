# PythonFlaskVulnerableApp
This is going to be a simple Python web server with some simple vulnerabilities.


This is going to be running on your computer so tread carefully when running exploits that you don't understand.  This is an exploitable application so be sure to take proper precautions when running it on your computer.


The goal of this project is to make a python web server that could be easily downloaded and ran for practice/testing/tool trials that
does not require the user to spin up a whole web server or anything special such as that it is going to be its own little module.

Current Vulnerabilities in the system and planned:
- [x] Reflected XSS
- [x] Stored XSS
- [x] Simple SQL Injection
- [x] Blind SQL Injection
- [x] File Path Traversal
- [ ] File Upload/Download
- [x] Shell execution

Always open to suggestions on any that you would like to see.

Technologies used
- Python 3
- [Flask](http://flask.pocoo.org/)
- SQLite

Folder Structure
```
-dbs (Just a folder for holding the databases that get created by the scripts)

-setup (hold files that will run on first startup of site or on reset to setup/reset the db's
|--db (Holds the database setup scripts)

-static (all the static such as css, images, js, etc)
|--css
|--js
|--fonts
|--images

-templates (All the templates for the pages including the basetemplate that all other templates extend.  Templates are broke out into sections)
|--sqli (sql injection section templates)
|--xss (xss section templates)

run.py (start place for the server, and the routes code)
```
