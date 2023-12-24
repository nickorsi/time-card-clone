import os  # ---> When using SQL Alchmey

from models import db, connect_db, Staff


from flask import Flask, request, render_template, redirect, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension  # ---> Debugger tool
from forms import CSRFForm, SignupStaff, LogInForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
# ---> Switch for redirect pause page, False=off True=on
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.debug = True  # ---> Switch for debug toolbar, False=off True=on

debug = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "[DATABASE_URL]", 'postgresql:///timecard_clone')
# ---> When using SQL Alchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True  # ---> When using SQL Alchemy

connect_db(app)  # ---> When using SQL Alchemy

CURR_USER_KEY = "curr_user"

################################################################################
# Routes Dealing with Login/Signup Security


@app.before_request
def save_user_to_g():
    """If logged in, add user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = Staff.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


@app.before_request
def save_csrf_to_g():
    """Saves csrf token to Flask global to add onto POST requests without
    dedicated Flask WTforms."""

    g.csrf_form = CSRFForm()


def log_in(user):
    """Assign valid user to session."""

    session[CURR_USER_KEY] = user.id



def log_out():
    """Removes user from session"""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
        g.user = None


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle staff signup

    Create new user, add to DB, redirect to hom page.

    If form not valid, present form with applicable errors.
    """

    log_out()

    form = SignupStaff()

    if form.validate_on_submit():
        try:
            staff = Staff.register(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                password=form.password.data,
                clearance=0,
            )
            db.session.commit()

        except IntegrityError:
            flash("Email already in system, please login in if you are the" +
                  " user or use another email to signup.", 'danger')
            return render_template("staff/signup.html", form=form)

        log_in(staff)

        return redirect("/")
    else:
        return render_template("staff/signup.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles authorized secure logins"""

    if g.user:
        return redirect("/")

    form = LogInForm()

    if form.validate_on_submit():
        print("HERE")
        staff = Staff.authenticate(
            email=form.email.data,
            password=form.password.data,
        )

        if staff:
            log_in(staff)
            flash('Logged in successfully!', 'success')
            return redirect('/')

        flash('Incorrect credentials.', 'danger')

    return render_template('staff/login.html', form=form)


@app.post('/logout')
def logout():
    """Process authorized and secure logout post"""

    form = g.csrf_form

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    if form.validate_on_submit:
        log_out()
        flash('You have successfully logged out!', 'success')

    return redirect('/')

################################################################################
# Staff and staff details

@app.get('/staff')
def show_staff():
    """Shows table of staff members.
    If user is not an admin, only shows active staff.
    If user is admin, shows all staff in system.
    """
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    search = request.args.get("q")

    if search:
        staff = Staff.query.filter(Staff.first_name.like(f"%{search}%")).all()
    else:
        staff = Staff.query.all()

    return render_template('staff/all-staff.html', staff=staff)

################################################################################
# Home route

@app.get('/')
def home():
    """Shows homepage.

    Logged in user will have links to available projects
    None logged in will have link to signup.
    """

    if g.user:
        return render_template('home.html')

    else:
        return render_template('home-non-user.html')
