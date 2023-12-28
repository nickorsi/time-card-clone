import os  # ---> When using SQL Alchmey

from models import db, connect_db, Staff, Project, DailyReport


from flask import Flask, request, render_template, redirect, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension  # ---> Debugger tool
from forms import CSRFForm, SignupStaffFrom, LogInForm, EditStaffForm
from forms import NewProjectForm, EditProjectForm
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
        staff = Staff.query.filter(Staff.first_name.ilike(f"%{search}%")).all()
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
        # Made readonly fields to prevent user from changing fields they
        # shouldn't, but if they change html with dev tools have checks to make
        # sure what should stay the same stays the same
        if g.user.clearance < 5:
            if (form.clearance.data != staff.clearance or
                form.status.data != staff.status):
                flash('You do not have clearance for these edits!', 'danger')
                return render_template(
                    'staff/edit-details.html',
                    form=form, staff=staff
                )

        if g.user.id != staff.id:
            if (form.first_name.data != staff.first_name or
                form.last_name.data != staff.last_name):
                flash('You do not have clearance for these edits!', 'danger')
                return render_template(
                    'staff/edit-details.html',
                    form=form, staff=staff
                )

        form.populate_obj(staff)

        db.session.commit()

        # If employee is now inactive, their roles must also be inactive.
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
        projects = Project.query.filter(Project.name.ilike(f"%{search}%")).all()
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
        # Made readonly field for project code to prevent user from changing
        # the auto generation and making a project code that isn't sequential.
        # Below check is to make sure the field hasn't changed if readonly
        # modified with dev tool.
        if form.code.data != new_code:
            flash('You do not have clearance to edit the project code!', 'danger')
            return render_template(
                'projects/new-project.html',
                form=form,
                new_code=new_code
            )
        # Still try making the project add in case another user is making a
        # project at the same exact time. Except the error and flash a message
        # to retry the process.
        try:
            project = Project(
                code = form.code.data,
                name = form.name.data,
                status = form.status.data,
            )

            db.session.add(project)

        except IntegrityError:
            flash("It looks like another project is already using this code." +
                  "Please cancel out and try again.", 'danger')
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

    if g.user.clearance < 4:
        if project_code not in user_project_ids or project.status == "inactive":
            flash("Access unauthorized.", "danger")
            return redirect("/")

    return render_template("projects/project-details.html", project=project)

@app.route('/projects/<project_code>/edit', methods=["GET", "POST"])
def edit_project(project_code):
    """Edit project details if clearance level 4 or above.
    Can only edit name and status.
    """

    if not g.user or g.user.clearance < 4:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    project = Project.query.get_or_404(f'{project_code}')

    form = EditProjectForm(obj=project)

    if form.validate_on_submit():
        if form.code.data != project.code:
            flash('You do not have clearance to edit the project code!', 'danger')
            return render_template(
                'projects/edit-project-details.html',
                form=form,
            )

        form.populate_obj(project)

        db.session.commit()

        # If project is now inactive, all roles must also be inactive.
        if project.status == "inactive":
            for role in project.staff_roles:
                role.status = "inactive"

        db.session.commit()

        flash('Edits made!', 'success')

        return redirect(f'/projects/{project.code}')

    return render_template('projects/edit-project-details.html', form=form)


################################################################################
# Time Cards

@app.get('/projects/<project_code>/daily-reports')
def show_daily_reports(project_code):
    """Shows list of daily reports associated with project
    Must have clearance of at least 1 to see reports and create new ones on
    active projects
    Must have clearance of at least 4 to see reports on all projects
    """

    if not g.user or g.user.clearance < 1:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    project = Project.query.get_or_404(f'{project_code}')

    if g.user.clearance < 4 and project.status == "inactive":
        flash("Access unauthorized.", "danger")
        return redirect("/projects")

    search = request.args.get("q")

    if search:
        filter_reports = DailyReport.query.filter(
            DailyReport.name.ilike(f"%{search}%")
        )
        filter_reports = filter_reports.filter(
            DailyReport.project_code == project_code
        )
        reports = filter_reports.all()
    else:
        reports = project.daily_reports

    return render_template(
        'daily-reports/all-daily-reports.html',
        reports=reports,
        project=project
    )

@app.route(
    '/projects/<project_code>/daily-reports/new',
    methods=["GET","POST"],
)
def new_daily_report(project_code):
    """Handle new daily report

    Must have clearance of at least 1 to see reports and create new ones on
    active projects
    Must have clearance of at least 4 to see reports on all projects
    """

    if not g.user or g.user.clearance < 1:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    project = Project.query.get_or_404(f'{project_code}')

    if g.user.clearance < 4 and project.status == "inactive":
        flash("Access unauthorized.", "danger")
        return redirect("/projects")

    return render_template('daily-reports/new-daily-report.html', project=project)

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
