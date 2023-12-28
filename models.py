from flask_sqlalchemy import SQLAlchemy

from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

DEFAULT_USER_IMAGE = ("https://upload.wikimedia.org/wikipedia/commons/b/b5/" +
"Windows_10_Default_Profile_Picture.svg")

def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)


class Project(db.Model):
    """Projects in the system.
    Relationships built to the following classes:
    -StaffRole (join table)
    -Staff
    -CraftRole (join table)
    -Craft
    -CostCode
    -DailyReport
    """

    __tablename__ = "projects"

    # Made project code a 6 character string rather than int with auto serial
    # increment. Did this to make all project codes a number but be consistent
    # in number length. For example 1 vs 000001, 2 vs 000002, etc. This makes it
    # easier for lookup creates consistancy with the codes while allowing for
    # lots of project availablity. But makes the creation and uniqueness more
    # work in the code.
    code = db.Column(
        db.String(6),
        primary_key=True,
    )

    name = db.Column(
        db.String(50),
        nullable=False,
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="active",
    )

    staff = db.relationship(
        'Staff',
        secondary="staff_roles",
        backref="projects"
    )

    craft = db.relationship(
        'Craft',
        secondary="craft_roles",
        backref="projects"
    )

    cost_codes = db.relationship(
        'CostCode',
        backref="project"
    )

    daily_reports = db.relationship(
        'DailyReport',
        order_by="DailyReport.date",
        backref="project"
    )


class Staff(db.Model):
    """Staff members in the system.
    Relationships built to the following classes:
    -StaffRole (join table)
    -Project
    -DailyReport
    """

    __tablename__ = "staff"

    __table_args__ = (
        db.UniqueConstraint("first_name", "last_name"),
    )

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    first_name = db.Column(
        db.String(30),
        nullable=False,
    )

    last_name = db.Column(
        db.String(30),
        nullable=False,
    )

    email = db.Column(
        db.String(50),
        nullable=False,
        unique=True,
    )

    image_url = db.Column(
        db.String(255),
        nullable=False,
        default=DEFAULT_USER_IMAGE,
    )

    password = db.Column(
        db.String(100),
        nullable=False,
    )

    clearance = db.Column(
        db.Integer,
        db.ForeignKey('clearances.level'),
        nullable=False,
        default=0,
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default='active',
    )


    daily_reports = db.relationship('DailyReport', backref='author')

    def __repr__(self):
        return f"<Staff #{self.id}: {self.first_name}, {self.last_name}, {self.email}, {self.clearance}>"

    @classmethod
    def register(
        cls,
        first_name,
        last_name,
        email,
        password,
        image_url=DEFAULT_USER_IMAGE,
        clearance=0,
        status="active"
    ):
        """Register a staff person.

        Hashes password and adds user to session.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        staff = Staff(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_pwd,
            image_url=image_url,
            clearance=clearance,
            status=status,
        )

        db.session.add(staff)

        return staff

    @classmethod
    def authenticate(cls, email, password):
        """Find user with `email` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for staff whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If this can't find matching staff (or if password is wrong), returns
        False.
        """

        staff = cls.query.filter_by(email=email).one_or_none()

        if staff and staff.status == "active":
            is_auth = bcrypt.check_password_hash(staff.password, password)
            if is_auth:
                return staff

        return False


class StaffRole(db.Model):
    """Staff Roles in the System.
    Acts as a join table for Staff and Project
    """

    __tablename__ = "staff_roles"

    project_code = db.Column(
        db.String(20),
        db.ForeignKey('projects.code'),
        primary_key=True,
    )

    staff_id = db.Column(
        db.Integer,
        db.ForeignKey('staff.id'),
        primary_key=True,
    )

    role = db.Column(
        db.String(50),
        nullable=False,
        default="",
    )

    status = db.Column(
        db.String(50),
        nullable=False,
        default="active"
    )

    project = db.relationship('Project', backref="staff_roles")
    staff = db.relationship('Staff', backref="staff_roles")


class Craft(db.Model):
    """Craft members in the system.
    Relationships built to the following classes:
    -CraftRole (join table)
    -Project
    """

    __tablename__ = "craft"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    first_name = db.Column(
        db.String(30),
        nullable=False,
    )

    last_name = db.Column(
        db.String(30),
        nullable=False,
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="active",
    )

    @classmethod
    def register(cls, first_name, last_name):
        """Register a craft person.
        """

        craft = Craft(
            first_name=first_name,
            last_name=last_name,
        )

        db.session.add(craft)

        return craft


class CraftRole(db.Model):
    """Craft Roles in the System.
    Acts as a join table for Craft and Project
    """

    __tablename__ = "craft_roles"

    project_code = db.Column(
        db.String(20),
        db.ForeignKey('projects.code'),
        primary_key=True,
    )

    craft_id = db.Column(
        db.Integer,
        db.ForeignKey('craft.id'),
        primary_key=True,
    )

    craft_role = db.Column(
        db.String(50),
        nullable=False,
        default="",
    )

    project = db.relationship('Project', backref="craft_roles")
    craft = db.relationship('Craft', backref="craft_roles")


class CostCode(db.Model):
    """Cost codes saved in the system.
    Relationships built to the following classes:
    -Project
    -DailyReportItem (join table)
    -DailyReport
    -CostCodeSummary
    """

    __tablename__ = "cost_codes"

    # Made the code a string rather than an int. Same reasoning as for the
    # project codes.
    code = db.Column(
        db.String(20),
        primary_key=True,
        autoincrement=False,
    )

    name = db.Column(
        db.String(50),
        nullable=False,
    )

    project_code = db.Column(
        db.String(20),
        db.ForeignKey('projects.code'),
        nullable=False,
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="active",
    )

    budgeted_qty = db.Column(
        db.Integer,
        nullable=False,
    )

    qty_units = db.Column(
        db.String(10),
        nullable=False,
    )

    budgeted_mhrs = db.Column(
        db.Integer,
        nullable=False,
    )

    budgeted_cost = db.Column(
        db.Integer,
        nullable=False,
    )


class Clearance(db.Model):
    """Clearance levels saved in the system.
    Relationships built to the following classes:
    -Staff
    """

    __tablename__ = "clearances"

    level = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=False,
    )

    name = db.Column(
        db.String(20),
        nullable=False,
    )


class DailyReport(db.Model):
    """Daily Reports in the system.
    Relationships built to the following classes:
    -Project
    -Staff
    -DailyReportItem
    -CostCodeSummary
    -CraftSummary
    """

    __tablename__ = "daily_reports"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    name = db.Column(
        db.String(50),
        nullable=False,
    )

    date = db.Column(
        db.Date,
        nullable=False,
    )

    project_code = db.Column(
        db.String(20),
        db.ForeignKey('projects.code'),
        nullable=False,
    )

    author_id = db.Column(
        db.Integer,
        db.ForeignKey('staff.id'),
        nullable=False,
    )

    approver_id = db.Column(
        db.Integer,
        nullable=False,
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="started",
    )

    hrs = db.relationship(
        'DailyReportItem',
        backref="daily_report"
    )

    code_details = db.relationship(
        'CostCodeSummary',
        backref="daily_reports",
    )

    craft_notes = db.relationship(
        'CraftSummary',
        backref="daily_report",
    )


class DailyReportItem(db.Model):
    """Daily Report Items in the system.
    Relationships built with the following classes:
    -DailyReport
    """

    __tablename__ = "daily_report_items"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    daily_report_id = db.Column(
        db.Integer,
        db.ForeignKey('daily_reports.id'),
        nullable=False,
    )

    craft_id = db.Column(
        db.Integer,
        db.ForeignKey('craft.id'),
        nullable=False,
    )

    cost_code = db.Column(
        db.String(20),
        db.ForeignKey('cost_codes.code'),
        nullable=False,
    )

    hrs_worked = db.Column(
        db.Integer,
        nullable=False,
    )


class CostCodeSummary(db.Model):
    """Cost Code Summaries in the system.
    Relationships built with the following classes:
    -DailyReport
    """

    daily_report_id = db.Column(
        db.Integer,
        db.ForeignKey('daily_reports.id'),
        primary_key=True,
    )

    cost_code = db.Column(
        db.String(20),
        db.ForeignKey('cost_codes.code'),
        primary_key=True,
    )

    qty_installed = db.Column(
        db.Integer,
        nullable=False,
    )

    note = db.Column(
        db.String(500),
        nullable=False,
    )


class CraftSummary(db.Model):
    """Craft Summaries in the system.
    Relationships built with the following classes:
    -DailyReport
    """

    daily_report_id = db.Column(
        db.Integer,
        db.ForeignKey('daily_reports.id'),
        primary_key=True,
    )

    craft_id = db.Column(
        db.Integer,
        db.ForeignKey('craft.id'),
        primary_key=True,
    )

    note = db.Column(
        db.String(500),
        nullable=False,
    )
