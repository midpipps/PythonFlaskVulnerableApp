from flask import Flask, render_template, request
from setup import db
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/xss/reflected/', methods=['GET', 'POST'])
def reflected(name = None):
    if (request.values.get('name')):
        name = request.values['name']
    return render_template('./xss/reflected.html', name=name)

if __name__=='__main__':
    db.run(False)
    app.run(debug=True, host='0.0.0.0')
