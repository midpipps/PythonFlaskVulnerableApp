from flask import Flask, render_template, request, redirect, url_for
from setup.db import db, xss, sqlinjection
import logging
from logging import StreamHandler
app = Flask(__name__)

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
    return render_template('./xss/reflected.html', name=name)

@app.route('/xss/stored/', methods=['GET', 'POST'])
def xss_stored():
    if request.method == 'POST':
        name = request.form['name']
        comment = request.form['comment']
        parentID = request.form['parentID']
        if name and comment:
            xss.addComment(name, comment, parentID)
    all_rows = xss.getComments()
    return render_template('./xss/stored.html', comments=all_rows)
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
    return render_template('./sqli/simple.html', comments = comments, search = search)
#**************
#End SQLI Routes
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
