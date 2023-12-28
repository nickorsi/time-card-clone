from models import Project, Staff, StaffRole, Craft, CraftRole, CostCode
from models import DailyReport, DailyReportItem, CostCodeSummary, CraftSummary
from models import Clearance, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# Create project

project1 = Project(
    code='100000',
    name='Gross Reservoir',
)

db.session.add(project1)
db.session.commit

project2 = Project(
    code='100001',
    name='Hell Hole',
    status="inactive"
)

db.session.add(project2)
db.session.commit

# Create clearance levels

clr0 = Clearance(
    level=0,
    name='None'
)

db.session.add(clr0)
db.session.commit()

clr1 = Clearance(
    level=1,
    name='Eng'
)

db.session.add(clr1)
db.session.commit()

clr2 = Clearance(
    level=2,
    name='Sup'
)

db.session.add(clr2)
db.session.commit()

clr3 = Clearance(
    level=3,
    name='Business'
)

db.session.add(clr3)
db.session.commit()

clr4 = Clearance(
    level=4,
    name='Project Eng'
)

db.session.add(clr4)
db.session.commit()

clr5 = Clearance(
    level=5,
    name='Admin'
)

db.session.add(clr5)
db.session.commit()

# Create staff

staff1 = Staff.register(
    first_name='Engineer',
    last_name='Test',
    email='engineer@gmail.com',
    clearance=1,
    password='engineer'
)

db.session.commit()

staff2 = Staff.register(
    first_name='Superintendent',
    last_name='Test',
    email='superintendent@gmail.com',
    clearance= 2,
    password='superintendent'
)

db.session.commit()

staff3 = Staff.register(
    first_name='Business',
    last_name='Test',
    email='business@gmail.com',
    clearance=3,
    password='business'
)

db.session.commit()

staff4 = Staff.register(
    first_name='Projecteng',
    last_name='Test',
    email='projecteng@gmail.com',
    clearance= 4,
    password='projecteng'
)

db.session.commit()

staff5 = Staff.register(
    first_name='Admin',
    last_name='Test',
    email='admin@gmail.com',
    clearance=5,
    password='adminadmin'
)

db.session.commit()

staff6 = Staff.register(
    first_name='Admin2',
    last_name='Test',
    email='admin2@gmail.com',
    clearance=5,
    password='adminadmin',
    status="inactive",
)

db.session.commit()

# Create Staff Roles

staff1.staff_roles.append(
    StaffRole(
        project_code=project1.code,
        role="Exc Engineer"
    )
)

db.session.commit()

staff2.staff_roles.append(
    StaffRole(
        project_code=project1.code,
        role="Exc Superintendent"
    )
)

db.session.commit()

staff3.staff_roles.append(
    StaffRole(
        project_code=project1.code,
        role="Business Controller"
    )
)

db.session.commit()

staff4.staff_roles.append(
    StaffRole(
        project_code=project1.code,
        role="Project Engineer"
    )
)

db.session.commit()

staff5.staff_roles.append(
    StaffRole(
        project_code=project1.code,
        role="Project Admin"
    )
)

db.session.commit()

staff5.staff_roles.append(
    StaffRole(
        project_code=project2.code,
        role="Project Admin"
    )
)

db.session.commit()

staff6.staff_roles.append(
    StaffRole(
        project_code=project2.code,
        role="Project Admin",
        status='inactive',
    )
)

db.session.commit()

# Create craft

craft1 = Craft.register(
    first_name='Foreman',
    last_name='Test'
)

db.session.commit()

craft2 = Craft.register(
    first_name='Operator',
    last_name='Test'
)

db.session.commit()

craft3 = Craft.register(
    first_name='Laborer',
    last_name='Test'
)

db.session.commit()

# Create craft roles

craft1.craft_roles.append(
    CraftRole(
        project_code=project1.code,
        craft_role="Exc Foreman"
    )
)

db.session.commit()

craft2.craft_roles.append(
    CraftRole(
        project_code=project1.code,
        craft_role="Exc Operator"
    )
)

db.session.commit()

craft3.craft_roles.append(
    CraftRole(
        project_code=project1.code,
        craft_role="Exc Laborer"
    )
)

db.session.commit()

## Create cost codes

code1 = CostCode(
    code="1000",
    name="Clear and Grub",
    project_code=project1.code,
    status="active",
    budgeted_qty=22500,
    qty_units="SF",
    budgeted_mhrs=20,
    budgeted_cost=3600
)

db.session.add(code1)
db.session.commit()

code2 = CostCode(
    code="1001",
    name="Excavate",
    project_code=project1.code,
    status="active",
    budgeted_qty=8333,
    qty_units="CY",
    budgeted_mhrs=42,
    budgeted_cost=7560
)

db.session.add(code2)
db.session.commit()

code3 = CostCode(
    code="1002",
    name="Haul/Dump Exc",
    project_code=project1.code,
    status="active",
    budgeted_qty=8333,
    qty_units="CY",
    budgeted_mhrs=420,
    budgeted_cost=33600
)

db.session.add(code3)
db.session.commit()

# Create daily report

daily1 = DailyReport(
    date="2023.12.21",
    name="Day 1: Clear and Exc",
    project_code="100000",
    author_id=staff1.id,
    approver_id=staff2.id,
    status="approved"
)

db.session.add(daily1)
db.session.commit()

# Create daily report items

item1 = DailyReportItem(
    daily_report_id=daily1.id,
    craft_id=craft1.id,
    cost_code=code1.code,
    hrs_worked=4
)

db.session.add(item1)
db.session.commit()

item2 = DailyReportItem(
    daily_report_id=daily1.id,
    craft_id=craft1.id,
    cost_code=code2.code,
    hrs_worked=4
)

db.session.add(item2)
db.session.commit()

item3 = DailyReportItem(
    daily_report_id=daily1.id,
    craft_id=craft1.id,
    cost_code=code3.code,
    hrs_worked=2
)

db.session.add(item3)
db.session.commit()

item4 = DailyReportItem(
    daily_report_id=daily1.id,
    craft_id=craft2.id,
    cost_code=code1.code,
    hrs_worked=5
)

db.session.add(item4)
db.session.commit()

item5 = DailyReportItem(
    daily_report_id=daily1.id,
    craft_id=craft2.id,
    cost_code=code2.code,
    hrs_worked=5
)

db.session.add(item5)
db.session.commit()

item6 = DailyReportItem(
    daily_report_id=daily1.id,
    craft_id=craft3.id,
    cost_code=code1.code,
    hrs_worked=2
)

db.session.add(item6)
db.session.commit()

item7 = DailyReportItem(
    daily_report_id=daily1.id,
    craft_id=craft3.id,
    cost_code=code2.code,
    hrs_worked=4
)

db.session.add(item7)
db.session.commit()

item8 = DailyReportItem(
    daily_report_id=daily1.id,
    craft_id=craft3.id,
    cost_code=code3.code,
    hrs_worked=4
)

db.session.add(item8)
db.session.commit()

# Create cost code summaries

code_summary1 = CostCodeSummary(
    daily_report_id=daily1.id,
    cost_code=code1.code,
    qty_installed=22500,
    note="Started and finished grubbing site today."
)

db.session.add(code_summary1)
db.session.commit()

code_summary2 = CostCodeSummary(
    daily_report_id=daily1.id,
    cost_code=code2.code,
    qty_installed=200,
    note="Started exc today, had to spend time setting up operation."
)

db.session.add(code_summary2)
db.session.commit()

code_summary3 = CostCodeSummary(
    daily_report_id=daily1.id,
    cost_code=code3.code,
    qty_installed=200,
    note="Started haul today, only got a single round of trucks out."
)

db.session.add(code_summary3)
db.session.commit()

# Create craft summaries

craft_summary1 = CraftSummary(
    daily_report_id=daily1.id,
    craft_id=craft1.id,
    note="No injuries, took all breaks and lunch."
)

db.session.add(craft_summary1)
db.session.commit()

craft_summary2 = CraftSummary(
    daily_report_id=daily1.id,
    craft_id=craft2.id,
    note="No injuries, took all breaks and lunch."
)

db.session.add(craft_summary2)
db.session.commit()

craft_summary3 = CraftSummary(
    daily_report_id=daily1.id,
    craft_id=craft3.id,
    note="No injuries, took all breaks and lunch."
)

db.session.add(craft_summary3)
db.session.commit()