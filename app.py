# Importing the modules
# Render_template Renders the HTML and Request handles form data
# Redirect and url_for direct users to route in the website navigation
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create a new Flask app
app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) # Will get the models and data

# Define Todo Model Class (models a to do list item that is stored in the database)
# Defines the columns (attributes) for the class
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    done = db.Column(db.Boolean, default = False)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)

    # Add the repr method
    # A special method that returns a string representing the object
    def __repr__(self):
        return f'<todo id="{self.id}" title="{self.title}" done="{self.done}" created_at="{self.created_at}">'