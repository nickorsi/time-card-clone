import os  # ---> When using SQL Alchmey

from models import db, connect_db, Staff, Project


from flask import Flask, request, render_template, redirect, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension  # ---> Debugger tool
from forms import CSRFForm, SignupStaffFrom, LogInForm, EditStaffForm
from forms import NewProjectForm
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

    form = SignupStaffFrom()

    if form.validate_on_submit():
        try:
            staff = Staff.register(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                image_url=form.image_url.data or Staff.image_url.default.arg,
                password=form.password.data,
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

@app.get('/staff/<int:staff_id>')
def show_staff_profile(staff_id):
    """Shows the profile of the specific staff member.
    Non admin users can see profile of all active staff, but only
    -First name
    -Last name
    -Current roles
    -Project Experience
    Users viewing their own profile can also see their
    -Clearane level
    -Employment status
    -Edit button
    Admins can see all of the above for both active and inactive employees and
    project, and roles.
    """

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    staff = Staff.query.get_or_404(f'{staff_id}')

    if g.user.clearance < 5 and staff.status != "active":
        flash("Access unauthorized.", "danger")
        return redirect("/")

    return render_template('staff/details.html', staff=staff)

@app.route('/staff/<int:staff_id>/edit', methods=["GET", "POST"])
def edit_staff(staff_id):
    """ Handles user edits.
    If user editing their own profile, can edit name.
    If user is admin, can edit only clearance level and status.
    """

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    staff = Staff.query.get_or_404(f'{staff_id}')

    if g.user.clearance < 5 and staff.status != "active":
        flash("Access unauthorized.", "danger")
        return redirect("/")


    form = EditStaffForm(obj=staff)

    if form.validate_on_submit():
        form.populate_obj(staff)

        db.session.commit()

        if staff.status == "inactive":
            for role in staff.staff_roles:
                role.status = "inactive"

        db.session.commit()

        flash('Edits made!', 'success')

        return redirect(f'/staff/{staff_id}')

    return render_template('staff/edit-details.html', form=form, staff=staff)

################################################################################
# Projects and Project details

@app.get('/projects')
def show_projects():
    """Show list of projects.
    Only show list of assigned projects for users below clearance level 4
    Show all projects for users clearance level 4 and above"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    search = request.args.get("q")

    if search:
        projects = Project.query.filter(Project.name.like(f"%{search}%")).all()
    else:
        projects = Project.query.all()

    return render_template('projects/all-projects.html', projects=projects)

@app.route('/projects/new', methods=["GET", "POST"])
def new_project():
    """Handle creation of a new project.
    Must be clearance level 4 or above to create new project.
    """

    if not g.user or g.user.clearance < 4:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = NewProjectForm()

    last_project = Project.query.order_by(Project.code.desc()).first()

    new_code = int(last_project.code)+1

    if form.validate_on_submit():

        try:
            project = Project(
                code = form.code.data,
                name = form.name.data,
                status = form.status.data,
            )

            db.session.add(project)

        except IntegrityError:
            flash("The code must be 6 numbers long and be the very next" +
                   "available project number.", 'danger')
            return render_template("staff/signup.html", form=form)

        db.session.commit()

        flash('Project made!', 'success')

        return redirect('/projects')

    return render_template(
        'projects/new-project.html',
        form=form,
        new_code=new_code
    )

@app.get('/projects/<project_code>')
def show_project(project_code):
    """Show the homepage for the specific project.

    If the user is under clearance level 4, project must be assigned to them
    and be active for authorized access.
    If user is clearance level 4 and above, can view all projects.
    """

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    project = Project.query.get_or_404(f'{project_code}')

    user_project_ids = [project.code for project in g.user.projects]

    if project_code not in user_project_ids or project.status == "inactive":
        flash("Access unauthorized.", "danger")
        return redirect("/")

    return render_template("projects/project-details.html", project=project)


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
