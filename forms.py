from flask_wtf import FlaskForm #---> Make forms by subclassing off of the FlaskForm class, includes CSRF token in forms

from wtforms import StringField, PasswordField #---> Import field types such as StringField and PasswordField

from wtforms.validators import InputRequired, Email, Length #---> Import validator methods such as InputRequired, Email, and Length
from wtforms.validators import ValidationError

def not_empty(form,field):
    """Checks field data isn't empty after striped"""
    if field.data.strip() == "":
        raise ValidationError('Field cannot be left blank.')

def num_like(form,field):
    """Checks field data can convert to a number"""
    try:
        int(field.data)
    except ValueError:
        raise ValidationError('Must only have numbers in field.')


class SignupStaff(FlaskForm):
    """Signup Staff Form"""

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

class LogInForm(FlaskForm):
    """Staff Log In Form"""

    email = StringField(
        "Email",
        validators=[InputRequired(), Email()]
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min = 8, max = 50)]
    )

class ProjectForm(FlaskForm):
    """Project Form"""

    code = StringField(
        "Project Code",
        validators=[InputRequired(),Length(min=6),num_like]
    )

    name = StringField(
        "Project Name",
        validators=[InputRequired(), not_empty, Length(max=50)]
    )

class CSRFForm(FlaskForm):
    """Form solely meant to genrate a CSRF token."""
