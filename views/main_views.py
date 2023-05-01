from flask import render_template
from models import Task, TaskCategory, GroceryItem, GroceryCategory

def index():
    task_categories = TaskCategory.query.all()
    tasks = Task.query.filter_by(completed=False).all()
    completed_tasks = Task.query.filter_by(completed=True).all()
    
    grocery_categories = GroceryCategory.query.all()
    grocery_items = GroceryItem.query.filter_by(completed=False).all()
    completed_grocery_items = GroceryItem.query.filter_by(completed=True).all()
    
    return render_template('index.html', task_categories=task_categories, tasks=tasks, completed_tasks=completed_tasks, grocery_categories=grocery_categories, grocery_items=grocery_items, completed_grocery_items=completed_grocery_items)