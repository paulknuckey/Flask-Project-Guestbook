import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdfasdf'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Guest(db.Model):
    __tablename__ = 'Guest'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True, index = True)
    message = db.Column(db.Text(64), nullable = True)

class GuestForm(FlaskForm):
    name = StringField('What is your Name?', validators=[DataRequired()])
    message = TextAreaField('Enter your message:', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
@app.route('/', methods =
['GET', 'POST'])
def index():
   form = GuestForm()
   if form.validate_on_submit():

 #       name = Guest.query.filter_by(name=form.name.data).first() looking for name in db
        
        name = Guest(name = form.name.data, message = form.message.data)
        db.session.add(name)
        db.session.commit()
        form.name.data = ''
        form.message.data = ''

    #query the Guest table for all entries and store that in an object
   myGuest = Guest.query.all()
   
   return render_template('main.html', form=form, myGuest=myGuest) #also pass those Guest entries to your template




if __name__ == '__main__':
    app.run(debug=True)