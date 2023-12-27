from flask_wtf import FlaskForm #---> Make forms by subclassing off of the FlaskForm class, includes CSRF token in forms

from wtforms_alchemy import model_form_factory

from wtforms import StringField, PasswordField, IntegerField, SelectField #---> Import field types such as StringField and PasswordField

from wtforms.validators import InputRequired, Email, Length, AnyOf
from wtforms.validators import ValidationError, Optional, URL

from models import db, Project

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


class SignupStaffFrom(FlaskForm):
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

    image_url = StringField(
        "Image URL",
        validators=[Optional(), URL(), Length(max=250)]
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

class EditStaffForm(FlaskForm):
    """Edit Staff Form"""

    first_name = StringField(
        "First Name",
        validators=[InputRequired(), not_empty, Length(max=30)]
    )

    last_name = StringField(
        "Last Name",
        validators=[InputRequired(), not_empty, Length(max=30)]
    )

    clearance = IntegerField(
        "Clearance Lvel",
        validators=[InputRequired(), AnyOf(values=[0,1,2,3,4,5])]
    )

    status = SelectField(
        "Employment Status",
        choices=[("active", "Active"), ("inactive", "Inactive")],
        validators=[InputRequired()]
    )

class CSRFForm(FlaskForm):
    """Form solely meant to genrate a CSRF token."""

# BaseModelForm = model_form_factory(FlaskForm)

# class ModelForm(BaseModelForm):
#     """Form estbalished to make forms from model files."""

#     @classmethod
#     def get_session(self):
#         return db.session

# class NewProjectForm(ModelForm):
#     """Make new project"""

#     class Meta:
#         model = Project

class NewProjectForm(FlaskForm):
    """Make new project"""

    code = StringField(
        "Project Code",
        validators=[InputRequired(), not_empty, num_like, Length(min=6, max=6)]
    )

    name = StringField(
        "Project Name",
        validators=[InputRequired(), not_empty, Length(max=50)]
    )

    status = SelectField(
        "Project Status",
        choices=[("active", "Active"), ("inactive", "Inactive")],
        validators=[InputRequired()]
    )