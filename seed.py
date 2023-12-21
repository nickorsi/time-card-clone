from models import [Classes], db #---> For making instances of a class to make records in the table
from app import app

# Create all tables
db.drop_all()
db.create_all()