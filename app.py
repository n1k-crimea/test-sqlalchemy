from collections import namedtuple
from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

Message = namedtuple('Message', 'text tag')
messages = []


@app.route('/')
def index_page():
    return render_template('index.html')


@app.route('/message')
def msg_page():
    return render_template('message.html', messages=messages)

@app.route('/add_message', methods=['POST'])
def add_msg():
    text = request.form.get('text')
    tag = request.form.get('tag')
    messages.append(Message(text, tag))
    return redirect(url_for('msg_page'))

if __name__ == '__main__':
    app.run(debug=True)
