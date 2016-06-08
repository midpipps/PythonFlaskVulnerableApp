from flask import Flask, render_template
from setup import db
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


if __name__=='__main__':
    db.run(False)
    app.run(debug=True, host='0.0.0.0')
