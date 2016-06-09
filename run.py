from flask import Flask, render_template, request
from setup.db import db, xss
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/xss/reflected/', methods=['GET', 'POST'])
def xss_reflected():
    if (request.values.get('name')):
        name = request.values['name']
    return render_template('./xss/reflected.html', name=name)

@app.route('/xss/stored/', methods=['GET', 'POST'])
def stored():
    all_rows = xss.getComments()
    return render_template('./xss/stored.html', comments=all_rows)

@app.template_filter('commentCut')
def commentCut(comments, id):
    if id == 0:
        id = None
    print(id)
    if comments:
        return (x for x in comments if x[4] == id)

if __name__=='__main__':
    db.create(False)
    app.run(debug=True, host='0.0.0.0')
