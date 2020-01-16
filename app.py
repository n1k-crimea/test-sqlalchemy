from collections import namedtuple
from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1024), nullable=False)
    def __init__(self, text, tags):
        self.text = text.strip()
        self.tags = [Tag(text=tag.strip()) for tag in tags.split(',')]

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1024), nullable=False)
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'), nullable=False)
    message = db.relationship('Message', backref=db.backref('tags', lazy=True))

db.create_all()

@app.route('/')
def index_page():
    return render_template('index.html')


@app.route('/message')
def msg_page():
    return render_template('message.html', messages=Message.query.all())

@app.route('/add_message', methods=['POST'])
def add_msg():
    text = request.form.get('text')
    tag = request.form.get('tag')
    db.session.add(Message(text, tag))
    db.session.commit()
    return redirect(url_for('msg_page'))

if __name__ == '__main__':
    app.run(debug=True)
