from csv import DictReader
from app import db
from models import User, Recipe, Saved_Recipe, Ingredient, Saved_Ingredient, List, List_Ingredient


db.drop_all()
