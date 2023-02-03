from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.model):
    """"User model"""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key = True
    )

    username = db.Column(
        db.String(30),
        unique = True, 
        nullable = False
    )

    email = db.Column(
        db.Text,
        unique = True,
        nullable = False
    )

    password = db.Column(
        db.Text,
        nullable = False
    )

    profile_image_url = db.Column(
        db.Text 
    )

    saved_recipes = db.Column(
        db.Text
    )

class Recipe(db.Model):
    """table for recipes"""

    __tablename__ = 'recipes'

    id = db.Column(
        db.Integer,
        primary_key = True
    )

    recipe_id = db.Column(
        db.Integer,
        nullable = False
    )

class Saved_Recipe(db.Model):
    """"table to connect users to recipes"""

    __tablename__ = 'saved_recipes'

    user_saving_recipe = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete = 'cascade'),
        primary_key = True
    )

    recipe_saved = db.Column(
        db.Integer,
        db.ForeignKey('recipes.id', ondelete = 'cascade'),
        primary_key = True
    )

class Ingredient(db.Model):
    """Table for ingredients"""

    __tablename__ = 'ingredients'

    id = db.Column(
        db.Integer,
        primary_key = True
    )

    ingredient_id = db.Column(
        db.Integer,
        nullable = False
    )

class Saved_Ingredient(db.Model):
    """Table to connect users to saved ingredients"""

    __tablename__ = 'saved_ingredients'

    user_saving_ingredient = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete = 'cascade'),
        primary_key = True
    )

    recipe_saved = db.Column(
        db.Integer,
        db.ForeignKey('ingredients.id', ondelete = 'cascade'),
        primary_key = True
    )

class List(db.Model):
    """table for grocery lists"""

    __tablename__ = "lists"

    id = db.Column(
        db.Integer,
        primary_key = True
    )

    created_by = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )

class List_Ingredient:
    """"Table for joining ingredients to lists"""

    ___tablename__ = "list_ingredients"

    list_id = db.Column(
        db.Integer,
        db.ForeignKey('lists.id', ondelete = 'cascade'),
        primary_key = True
    )

    ingredient_id = db.Column(
        db.Integer,
        db.ForeignKey('ingredients.id', ondelete = 'cascade'),
        primary_key = True
    )


def connect_db(app):
    db.app = app
    db.init_app(app)