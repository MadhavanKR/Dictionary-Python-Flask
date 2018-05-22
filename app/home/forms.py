from flask_wtf import FlaskForm;
from wtforms import StringField,SubmitField;
from wtforms.validators import DataRequired;

class HomeForm(FlaskForm):
    word = StringField('Type the word',[DataRequired()]);
    submit = SubmitField('search');