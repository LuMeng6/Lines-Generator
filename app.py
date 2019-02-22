# Set up a local web server using Flask

import RNN
from flask import Flask
app = Flask(__name__)
from flask import render_template
from flask import request

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def login():
    res = None
    if request.method == 'POST':
        res = RNN.run(request.form['userMsg'])
    return res

if __name__ == '__main__':
    app.run()