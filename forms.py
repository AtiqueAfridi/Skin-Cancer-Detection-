
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, FileField, TextAreaField
from wtforms.validators import DataRequired, Email, NumberRange

class PatientForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    contact = StringField('Contact Number', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=0, max=120)])
    skin_type = SelectField('Skin Type', choices=[
        ('type1', 'Type I (Very Fair)'),
        ('type2', 'Type II (Fair)'),
        ('type3', 'Type III (Medium)'),
        ('type4', 'Type IV (Olive)'),
        ('type5', 'Type V (Brown)'),
        ('type6', 'Type VI (Dark Brown to Black)')
    ], validators=[DataRequired()])
    lesion_location = StringField('Lesion Location', validators=[DataRequired()])
    image = FileField('Upload Image', validators=[DataRequired()])

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])
