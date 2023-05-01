from flask_sqlalchemy import SQLAlchemy

# Create an instance of SQLAlchemy and pass the Flask app instance 
db = SQLAlchemy()

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

