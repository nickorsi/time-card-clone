from flask_wtf import FlaskForm #---> Make forms by subclassing off of the FlaskForm class, includes CSRF token in forms

from wtforms import ... #---> Import field types such as StringField and PasswordField

from wtforms.validators import ... #---> Import validator methods such as InputRequired, Email, and Length

class RegisterUserForm(FlaskForm): #---> Sample form
    """Register User Form"""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(max = 20)]
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min = 8, max = 20)] #max longer
    )