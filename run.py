from flask import Flask, render_template, send_from_directory, request, redirect, url_for, flash
from setup.db import db, xss, sqlinjection, fuzzing
from setup.file import fileaccess
from setup.execution import execute
import logging
import os
from logging import StreamHandler
app = Flask(__name__)
app.secret_key = 'someSecret'

#**************
#Misc Routes
#**************
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reset/')
def reset():
    db.create(True)
    return redirect(url_for('index'))
#**************
#End Misc Routes
#**************

#*************
#XSS Routes
#*************
@app.route('/xss/reflected/', methods=['GET', 'POST'])
def xss_reflected():
    name=None
    if (request.values.get('name')):
        name = request.values['name']
    return render_template('./xss/reflected.html', name = name)

@app.route('/xss/stored/', methods=['GET', 'POST'])
def xss_stored():
    if request.method == 'POST':
        name = request.form['name']
        comment = request.form['comment']
        parentID = request.form['parentID']
        if name and comment:
            xss.addComment(name, comment, parentID)
    all_rows = xss.getComments()
    return render_template('./xss/stored.html', comments = all_rows)
#**************
#End XSS Routes
#**************

#**************
#SQLI Routes
#**************
@app.route('/sqli/simple/', methods=['GET', 'POST'])
def sqli_simple():
    comments = None
    search = ''
    if request.method == 'POST':
        search = request.form['search']
    comments = sqlinjection.search(search)
    return render_template('./sqli/simple.html', comments = comments[1], search = search, sqlquery = comments[0])

@app.route('/sqli/simpleescape/', methods=['GET', 'POST'])
def sqli_simpleescape():
    comments = None
    search = ''
    if (request.method == 'POST'):
        search = request.form['search']
        search = search.replace(";--", " ")
    comments = sqlinjection.search(search)
    return render_template('./sqli/simpleescape.html', comments = comments[1], search = search, sqlquery = comments[0])

@app.route('/sqli/blind/', methods=['GET', 'POST'])
def sqli_blind():
    name = None
    phone = None
    secret = None
    display = 1
    if (request.method == 'POST'):
        name = request.form['name']
        phone = request.form['phone']
        secret = request.form['secret']
        if (name and phone and secret and display):
            flash('Your submission has been saved.', 'success')
            sqlinjection.search_insert(name, phone, secret)
        else:
            flash('Make sure you are filling out all the fields', 'error')
    return render_template('./sqli/blindinjection.html', name = name, phone = phone, secret = secret, display = display)

#**************
#End SQLI Routes
#**************

#**************
#File Routes
#**************
@app.route('/file/traversal/', methods=['GET'])
def file_traversal():
    current_path = fileaccess.os_getuploadspath()
    entered_path = ""
    file = None
    results = None
    if (request.values.get('path')):
        entered_path = request.values.get('path')
        current_path = os.path.join(current_path, *(entered_path.replace('\\', '/').split("/")))
    if (request.values.get('file')):
        file = request.values.get('file')
        if (fileaccess.os_fileexists(current_path, file)):
            return send_from_directory(current_path, file)
    results = fileaccess.os_getfilesandfolders(current_path)
    return render_template('./files/traversal.html', path = entered_path, results = results, file = file)
#**************
#End File Routes
#**************

#**************
# Execution Routes
#**************
@app.route('/execution/simple/', methods=['GET', 'POST'])
def execution_simple():
    ip = None
    results = None
    if request.method == 'POST':
        ip = request.form['ip']
        results = execute.execute_ping(ip)
    return render_template('./execution/simple.html', ip = ip, results = results)
#**************
#End Execution Routes
#**************

#**************
#Fuzzing Routes
#**************
@app.route('/fuzzing/simple/', methods=['GET'], defaults={'id':None})
@app.route('/fuzzing/simple/<int:id>/', methods=['GET'])
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
@app.template_filter('commentCut')
def commentCut(comments, id):
    if comments:
        return (x for x in comments if x[4] == id)
    return None
#**************
#End Filters
#**************

if __name__=='__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Starting db Creation")
    db.create(False)
    logging.info("DB creation script complete.\r\nStarting the server")
    app.run(debug=True, host='0.0.0.0')
