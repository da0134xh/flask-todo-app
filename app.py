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
db = SQLAlchemy(app) # Will get the models, columns, and data

# Define Todo Model Class (models a to-do-list item that is stored in the database)
# Defines the columns (attributes) for the class
class Todo(db.Model): # ORM that SQLAlchemy is doing on the fly
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    done = db.Column(db.Boolean, default = False)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)

    # Add the repr method
    # A special method that returns a string representing the object
    def __repr__(self):
        return f'<todo id="{self.id}" title="{self.title}" done="{self.done}" created_at="{self.created_at}">'
    
# Create the database and table to hold the "To Do"s
with app.app_context():
    db.create_all() #Creates a table in our SQLite database that models the Todo class (line 18).

# Create a home route that displays the To-do-list
@app.route('/')
def index():
    # Todo = model class that represents a table in database
    # .query = function that runs a select statement and returns a result set
    # .order_by() = orders the result set that is returned
    # .all = retrieves all the results of the query and returns them as a list
    todos = Todo.query.order_by(Todo.created_at.desc()).all()

    # This will be displayed in user's browser (jija engine)
    # Will apply the index.html to the result set of todos variable (line 40)
    # todos=todos - populate the todos in the template with the todos from the database
    return render_template('index.html', todos=todos)

# Create a route for adding a new To Do item to the database
@app.route('/add', methods=['POST'])
def add():
    #Get the title of the to do item from the HTML form on the web page
    title = request.form.get('title')

    # If the title IS NOT NULL, then create a new To Do List item record in the database
    # Else redirect the user to the index page (home page)
    if title:
        # Creates new to do object, using constructor. 
        # title atribute is populated by title passed by POST request
        new_todo = Todo(title=title) 
        db.session.add(new_todo) # Adds to database
        db.session.commit() # Commits transactions and saves
    return redirect(url_for('index'))

# Create a route for marking a To Do List item as done
@app.route('/toggle/<int:todo_id>')
def toggle(todo_id):
    # Update the database record and mark the To Do List as done
    # (if something goes wrong and the To Do List item doesn't exist, display a 404 error)
    todo = Todo.query.get_or_404(todo_id)
    # Mark the todo list item as done in the database
    todo.done = not todo.done #updates from the default 'False' to 'True' (not - not false)
    db.session.commit()
    return redirect(url_for('index'))

# Create a route to delete the To Do List item
@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    # Check if a database record exists with the ID number
    # and if there is no matching record, show a 404 error
    todo = Todo.query.get_or_404(todo_id)
    # Delete the record in the database for the Todo item
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

# Start the Flask app in debug mode
# Flask provides a debugger that shows a stack tract if an error
# Debug mode also reloads the page automatically when you make a chnage to the code
# you do not need to restart the server.
if __name__ == '__main__':
    # Starting in debug mode
    # Pass the todo id for the current to do list item
    # if todo id is present then it will pass along with http request
    app.run(debug=True)