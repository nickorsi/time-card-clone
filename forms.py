from flask_wtf import FlaskForm #---> Make forms by subclassing off of the FlaskForm class, includes CSRF token in forms

from wtforms import StringField, PasswordField #---> Import field types such as StringField and PasswordField

from wtforms.validators import InputRequired, Email, Length #---> Import validator methods such as InputRequired, Email, and Length
from wtforms.validators import ValidationError

def not_empty(form,field):
    """Checks field data isn't empty after striped"""
    if field.data.strip() == "":
        raise ValidationError('Field cannot be left blank.')

class RegisterStaff(FlaskForm):
    """Register Staff Form"""

    first_name = StringField(
        "First Name",
        validators=[InputRequired(), not_empty, Length(max=30)]
    )

    last_name = StringField(
        "Last Name",
        validators=[InputRequired(), not_empty, Length(max=30)]
    )

    email = StringField(
        "Email",
        validators=[InputRequired(), Email()]
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min = 8, max = 50)]
    )

class SignInForm(FlaskForm): #---> Sample form
    """Staff Sign In Form"""

    username = StringField(
        "Email",
        validators=[InputRequired(), Email()]
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min = 8, max = 50)]
    )