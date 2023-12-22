from models import Project, Staff, StaffRole, Craft, CraftRole, CostCode
from models import DailyReport, DailyReportItem, CostCodeSummary, CraftSummary
from models import Clearance, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# Create project

project = Project('100000', 'Gross Reservoir')

db.session.add(project)
db.session.commit

# Create clearance levels

clr1 = Clearance(1, 'Eng')

db.session.add(clr1)
db.session.commit()

clr2 = Clearance(2, 'Sup')

db.session.add(clr2)
db.session.commit()

clr3 = Clearance(3, 'Business')

db.session.add(clr3)
db.session.commit()

clr4 = Clearance(4, 'Project Eng')

db.session.add(clr4)
db.session.commit()

clr5 = Clearance(5, 'Admin')

db.session.add(clr5)
db.session.commit()

# Create staff

staff1 = Staff.register('Engineer', 'Test', 'engineer@gmail.com', 1, 'engineer')

db.session.commit()

staff2 = Staff.register(
    'Superintendent',
    'Test',
    'superintendent@gmail.com',
    2,
    'superintendent'
)

db.session.commit()

staff3 = Staff.register('Business', 'Test', 'business@gmail.com', 3, 'business')

db.session.commit()

staff4 = Staff.register(
    'Projecteng',
    'Test',
    'projecteng@gmail.com',
    4,
    'projecteng'
)

db.session.commit()

staff5 = Staff.register('Admin', 'Test', 'admin@gmail.com', 5, 'admin')

db.session.commit()

# Create Staff Roles

staff1.staff_roles.append(StaffRole(project_id=project.code, role="Exc Engineer"))

db.session.commit()

staff2.staff_roles.append(StaffRole(project_id=project.code, role="Exc Superintendent"))

db.session.commit()

staff3.staff_roles.append(StaffRole(project_id=project.code, role="Business Controller"))

db.session.commit()

staff4.staff_roles.append(StaffRole(project_id=project.code, role="Project Engineer"))

db.session.commit()

staff5.staff_roles.append(StaffRole(project_id=project.code, role="Project Admin"))

db.session.commit()

# Create craft

craft1 = Craft.register('Foreman', 'Test')

db.session.commit()

craft2 = Craft.register('Operator', 'Test')

db.session.commit()

craft3 = Craft.register('Laborer', 'Test')

db.session.commit()

# Create craft roles

craft1.craft_roles.append(CraftRole(project_id=project.code, role="Exc Foreman"))

db.session.commit()

craft2.craft_roles.append(CraftRole(project_id=project.code, role="Exc Operator"))

db.session.commit()

craft3.craft_roles.append(CraftRole(project_id=project.code, role="Exc Laborer"))

db.session.commit()

## Create cost codes

code1 = CostCode("1000", "Clear and Grub", project.code, 1, 22500, "SF", 20, 3600)

db.session.add(code1)
db.session.commit()

code2 = CostCode("1001", "Excavate", project.code, 1, 8333, "CY", 42, 7560)

db.session.add(code2)
db.session.commit()

code3 = CostCode("1002", "Haul/Dump Exc", project.code, 1, 8333, "CY", 420, 33600)

db.session.add(code3)
db.session.commit()

# Create daily report

daily1 = DailyReport("2023.12.21", staff1.id, staff2.id, "submitted")

db.session.add(daily1)
db.session.commit()

# Create daily report items

item1 = DailyReportItem(daily1.id, craft1.id, code1.code, 4)

db.session.add(item1)
db.session.commit()

item2 = DailyReportItem(daily1.id, craft1.id, code2.code, 4)

db.session.add(item2)
db.session.commit()

item3 = DailyReportItem(daily1.id, craft1.id, code3.code, 2)

db.session.add(item3)
db.session.commit()

item4 = DailyReportItem(daily1.id, craft2.id, code1.code, 5)

db.session.add(item4)
db.session.commit()

item5 = DailyReportItem(daily1.id, craft2.id, code2.code, 5)

db.session.add(item5)
db.session.commit()

item6 = DailyReportItem(daily1.id, craft3.id, code1.code, 2)

db.session.add(item6)
db.session.commit()

item7 = DailyReportItem(daily1.id, craft3.id, code2.code, 4)

db.session.add(item7)
db.session.commit()

item8 = DailyReportItem(daily1.id, craft3.id, code3.code, 4)

db.session.add(item8)
db.session.commit()

# Create cost code summaries

code_summary1 = CostCodeSummary(
    daily1.id,
    code1.code,
    22500,
    "Started and finished grubbing site today."
)

db.session.add(code_summary1)
db.session.commit()

code_summary2 = CostCodeSummary(
    daily1.id,
    code2.code,
    200,
    "Started exc today, had to spend time setting up operation."
)

db.session.add(code_summary2)
db.session.commit()

code_summary3 = CostCodeSummary(
    daily1.id,
    code3.code,
    200,
    "Started haul today, only got a single round of trucks out."
)

db.session.add(code_summary3)
db.session.commit()

# Create craft summaries

craft_summary1 = CraftSummary(
    daily1.id,
    craft1.id,
    "No injuries, took all breaks and lunch."
)

db.session.add(craft_summary1)
db.session.commit()

craft_summary2 = CraftSummary(
    daily1.id,
    craft2.id,
    "No injuries, took all breaks and lunch."
)

db.session.add(craft_summary2)
db.session.commit()

craft_summary3 = CraftSummary(
    daily1.id,
    craft3.id,
    "No injuries, took all breaks and lunch."
)

db.session.add(craft_summary3)
db.session.commit()