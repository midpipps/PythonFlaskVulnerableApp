'''
The start of the application has all the routes and the app invocation
'''
import os
import logging
from flask import Flask, render_template, send_from_directory, request, redirect, url_for, flash
from setup.db import db, xss, sqlinjection, fuzzing
from setup.file import fileaccess
from setup.execution import execute

APP = Flask(__name__)
APP.secret_key = 'someSecret'


#**************
#Misc Routes
#**************
@APP.route('/')
def index():
    '''
    Route handler for the home page
    '''
    return render_template('index.html')

@APP.route('/robots.txt')
def robots():
    '''
    Route handler for the home page
    '''
    return send_from_directory(APP.static_folder, 'robots.txt')

@APP.route('/mysecret/')
def secret():
    '''
    Route handler for the home page
    '''
    return render_template('./mysecret.html')

@APP.route('/reset/')
def reset():
    '''
    Route handler page that resets the hole database
    '''
    db.create(True)
    return redirect(url_for('index'))
#**************
#End Misc Routes
#**************

#*************
#XSS Routes
#*************
@APP.route('/xss/reflected/', methods=['GET', 'POST'])
def xss_reflected():
    '''
    Route handler for the reflected cross site scripting
    '''
    name = None
    if request.values.get('name'):
        name = request.values['name']
    return render_template('./xss/reflected.html', name=name)

@APP.route('/xss/stored/', methods=['GET', 'POST'])
def xss_stored():
    '''
    Route handler for the stored cross site scripting
    '''
    if request.method == 'POST':
        name = request.form['name']
        comment = request.form['comment']
        parentid = request.form['parentID']
        if name and comment:
            xss.addcomment(name, comment, parentid)
    all_rows = xss.getcomments()
    return render_template('./xss/stored.html', comments=all_rows)
#**************
#End XSS Routes
#**************

#**************
#SQLI Routes
#**************
@APP.route('/sqli/simple/', methods=['GET', 'POST'])
def sqli_simple():
    '''
    Route handler for the simple sql injection
    '''
    comments = None
    search = ''
    if request.method == 'POST':
        search = request.form['search']
    comments = sqlinjection.search(search)
    return render_template('./sqli/simple.html', comments=comments[1],
                           search=search, sqlquery=comments[0])

@APP.route('/sqli/simpleescape/', methods=['GET', 'POST'])
def sqli_simpleescape():
    '''
    Route handler for the simple sql escape injection
    '''
    comments = None
    search = ''
    if request.method == 'POST':
        search = request.form['search']
        search = search.replace(";--", " ")
    comments = sqlinjection.search(search)
    return render_template('./sqli/simpleescape.html', comments=comments[1],
                           search=search, sqlquery=comments[0])

@APP.route('/sqli/blind/', methods=['GET', 'POST'])
def sqli_blind():
    '''
    Route handler for the Blind sql injection page
    '''
    name = None
    phone = None
    secret = None
    display = 1
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        secret = request.form['secret']
        if name and phone and secret and display:
            flash('Your submission has been saved.', 'success')
            sqlinjection.search_insert(name, phone, secret)
        else:
            flash('Make sure you are filling out all the fields', 'error')
    return render_template('./sqli/blindinjection.html', name=name, phone=phone,
                           secret=secret, display=display)

#**************
#End SQLI Routes
#**************

#**************
#File Routes
#**************
@APP.route('/file/traversal/', methods=['GET'])
def file_traversal():
    '''
    Route handler for the file traversal page
    '''
    current_path = fileaccess.fileaccess_getuploadspath()
    entered_path = ""
    file = None
    results = None
    if request.values.get('path'):
        entered_path = request.values.get('path')
        current_path = os.path.join(current_path, *(entered_path.replace('\\', '/').split("/")))
    if request.values.get('file'):
        file = request.values.get('file')
        if fileaccess.fileaccess_fileexists(current_path, file):
            return send_from_directory(current_path, file)
    results = fileaccess.fileaccess_getfilesandfolders(current_path)
    return render_template('./files/traversal.html', path=entered_path, results=results, file=file)
#**************
#End File Routes
#**************

#**************
# Execution Routes
#**************
@APP.route('/execution/simple/', methods=['GET', 'POST'])
def execution_simple():
    '''
    Route handler for the execute simple page
    '''
    ip_address = None
    results = None
    if request.method == 'POST':
        ip_address = request.form['ip']
        results = execute.execute_ping(ip_address)
    return render_template('./execution/simple.html', ip=ip_address, results=results)
#**************
#End Execution Routes
#**************

#**************
#Fuzzing Routes
#**************
@APP.route('/fuzzing/simple/', methods=['GET'], defaults={'id':None})
@APP.route('/fuzzing/simple/<int:id>/', methods=['GET'])
def fuzzing_simple(id):
    data = None
    if id:
        data = fuzzing.getFuzzing(id)
    return render_template('./fuzzing/simple.html', data=data)
#**************
#End Execution Routes
#**************

#**************
#Filters
#**************
@APP.template_filter('commentcut')
def commentcut(comments, commentid):
    '''
    A filter used on the comments to get just
    the comments that pertain to the id
    '''
    if comments:
        return (x for x in comments if x[4] == commentid)
    return None
#**************
#End Filters
#**************

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Starting db Creation")
    db.create(False)
    logging.info("DB creation script complete.\r\nStarting the server")
    APP.run(debug=True, host='0.0.0.0')
