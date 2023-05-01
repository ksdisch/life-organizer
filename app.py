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
    # 'Category' db column for filtering
    category = db.Column(db.String(100), nullable=True)

    category_id = db.Column(db.Integer, db.ForeignKey('task_category.id'), nullable=True)
    category = db.relationship('TaskCategory', backref='tasks')


# Define a 'GroceryItem' class that inherits from 'db.Model' for creating a groceryitem model
class GroceryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    category = db.Column(db.String(100), nullable=True)

    category_id = db.Column(db.Integer, db.ForeignKey('grocery_category.id'), nullable=True)
    category = db.relationship('GroceryCategory', backref='grocery_items')

class TaskCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class GroceryCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)


# Define a route decorator for the root URL of the application
@app.route('/')
def index():
    task_categories = TaskCategory.query.all()
    tasks = Task.query.filter_by(completed=False).all()
    completed_tasks = Task.query.filter_by(completed=True).all()
    
    grocery_categories = GroceryCategory.query.all()
    grocery_items = GroceryItem.query.filter_by(completed=False).all()
    completed_grocery_items = GroceryItem.query.filter_by(completed=True).all()
    
    return render_template('index.html', task_categories=task_categories, tasks=tasks, completed_tasks=completed_tasks, grocery_categories=grocery_categories, grocery_items=grocery_items, completed_grocery_items=completed_grocery_items)


# Define a route decorator for user to add new tasks
@app.route('/add', methods=['POST'])
def add_task():
    title = request.form.get('title')
    category_name = request.form.get('category', 'Other')  # Get the category from the form, default to 'Other'
    
    # Query the category from the database or create a new one if it doesn't exist
    category = TaskCategory.query.filter_by(name=category_name).first()
    if not category:
        category = TaskCategory(name=category_name)
        db.session.add(category)
        db.session.commit()

    # Pass the category instance to the new item
    new_task = Task(title=title, category=category)

    db.session.add(new_task)  # Add the new 'Task' instance to the database session.
    db.session.commit()  # Commit the database session, which will save the new task to the database.

    return redirect(url_for('index'))  # Redirect the user back to the index page which should now have the new task.



# Define route decorator for '/toggle/<int:task_id>' URL, where 'task_id' is a variable that will be passed tot he view function. This route should only accept POST requests
@app.route('/toggle-task/<int:task_id>', methods=['POST'])
def toggle_task(task_id):
    # Query the task with the specified 'task_id' variable as an argument
    task = Task.query.get(task_id)
    
    # Get the task's status from the form data
    task_status = request.form.get('status')
    
    # Update the 'completed' attribute of the task based on the task's status
    if task_status == 'completed':
        task.completed = True
    else:
        task.completed = False
    
    # Commit the database session, which will save the updated task to the database.
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/add-grocery', methods=['POST'])
def add_grocery_item():
    title = request.form['title']
    category_name = request.form.get('category', 'Other')  # Get the category from the form, default to 'Other'

    # Query the category from the database or create a new one if it doesn't exist
    category = GroceryCategory.query.filter_by(name=category_name).first()
    if not category:
        category = GroceryCategory(name=category_name)
        db.session.add(category)
        db.session.commit()

    # Pass the category instance to the new item
    new_item = GroceryItem(name=title, category=category)

    db.session.add(new_item)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/toggle-grocery/<int:grocery_id>', methods=['POST'])
def toggle_grocery(grocery_id):
    # Query the grocery with the specified 'grocery_id' variable as an argument
    grocery = GroceryItem.query.get(grocery_id)
    
    # Get the grocery's status from the form data
    grocery_status = request.form.get('status')
    
    # Update the 'completed' attribute of the grocery based on the grocery's status
    if grocery_status == 'completed':
        grocery.completed = True
    else:
        grocery.completed = False
    
    # Commit the database session, which will save the updated grocery to the database.
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
