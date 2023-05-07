from flask import render_template
# from models import Task, TaskCategory, GroceryItem, GroceryCategory

def index():
    # # Retrieve task and grocery data from the database
    # task_categories = TaskCategory.query.all()
    # tasks = Task.query.filter_by(completed=False).all()
    # completed_tasks = Task.query.filter_by(completed=True).all()
    
    # grocery_categories = GroceryCategory.query.all()
    # grocery_items = GroceryItem.query.filter_by(completed=False).all()
    # completed_grocery_items = GroceryItem.query.filter_by(completed=True).all()
    
    # Render the index.html template with the retrieved data
    return render_template('index.html')
