from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask web app instance
app = Flask(__name__)
# Set the database URI to use a SQLite database named 'tasks.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
# Create an instance of SQLAlchemy and pass the Flask app instance 
db = SQLAlchemy(app)
# Define a 'Task' class that inherits from 'db.Model' for creating a task model
class Task(db.Model):
    # Create a primary key column 'id' with an integer data type
    id = db.Column(db.Integer, primary_key=True)
    # Create a 'title' column with a string data type and a max length of 100 characters, which cannot be null
    title = db.Column(db.String(100), nullable=False)
    # Create a 'completed' column with a boolean data type and a default value of False
    completed = db.Column(db.Boolean, default=False)

# Define a 'GroceryItem' class that inherits from 'db.Model' for creating a groceryitem model
class GroceryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)

# Define a route decorator for the root URL of the application
@app.route('/')
def index():
    tasks = Task.query.all()
    grocery_items = GroceryItem.query.all()
    return render_template('index.html', tasks=tasks, grocery_items=grocery_items)

# Define a route decorator for user to add new tasks
@app.route('/add', methods=['POST'])
# Define the 'add_task' view function to handle requests to the '/add' URL
def add_task():
    # Extract the 'title' field from the submitted form data using the 'request.form.get()' method
    title = request.form.get('title')
    # Create a new instance of the 'Task' class with the 'title' attribute set to the extracted 'title' from the form data.
    new_task = Task(title=title)
    # Add the new 'Task' instance to the database session.
    db.session.add(new_task)
    # Commit the database session, which will save the new task to the database.
    db.session.commit()
    # Redirect the user back to the index page which should now have the new task.
    return redirect(url_for('index'))

# Define route decorator for '/toggle/<int:task_id>' URL, where 'task_id' is a variable that will be passed tot he view function. This route should only accept POST requests
@app.route('/toggle/<int:task_id>', methods=['POST'])
# Define the 'toggle_task' view function to handle requests to the '/toggle/<int:task_id>' URL. This function takes the 'task_id' variable as an argument.
def toggle_task(task_id):
    # Query the task with the specified 'task_id' variable as an argument
    task = Task.query.get(task_id)
    # Toggle the 'completed' attribute of the task by negating its current value.
    task.completed = not task.completed
    # Commit the database session, which will save the updated task to the database.
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/add-grocery', methods=['POST'])
def add_grocery():
    name = request.form.get('name')
    new_grocery_item = GroceryItem(name=name)
    db.session.add(new_grocery_item)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/toggle-grocery/<int:item_id>', methods=['POST'])
def toggle_grocery(item_id):
    item = GroceryItem.query.get(item_id)
    item.completed = not item.completed
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
