import os
import socketserver as SocketServer

from flask import Flask, render_template, request, redirect, url_for, jsonify
# from flask.ext.bootstrap import Bootstrap
# from flask.ext.wtf import Form
# from flask.ext.sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Length



app = Flask(__name__)

app.config['SECRET_KEY'] = 'top secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

shopping_list = ['Milk', 'Eggs']

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required(),
                                                         Length(1, 16)])
    submit = SubmitField('Submit')


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), index=True, unique=True)

    def __repr__(self):
        return '<User {0}>'.format(self.name)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)
	
@app.route('/hello', methods=['GET', 'POST'])
def hello():
    name = None
    if request.method == 'POST' and 'name' in request.form:
        name = request.form['name']
    return render_template('hello.html', name=name)
	

@app.route('/greet', methods=['GET', 'POST'])
def greet():
    name = None
    new = False
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        if User.query.filter_by(name=name).first() is None:
            db.session.add(User(name=name))
            db.session.commit()
            new = True
    return render_template('greet.html', form=form, name=name, new=new)


@app.route('/shoppinglist', methods=['GET', 'POST'])
def shopping():
    global shopping_list
    if request.method == 'POST':
        shopping_list.append(request.form['item'])
    return render_template('shopping.html', items=shopping_list)


@app.route('/remove/<name>')
def remove_item(name):
    global shopping_list
    if name in shopping_list:
        shopping_list.remove(name)
    return redirect(url_for('shopping'))


@app.route('/api/items')
def get_items():
    global shopping_list
    return jsonify({'items': shopping_list})


if __name__=='__main__':
    db.create_all()
    app.run(debug=True)
