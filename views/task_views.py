from flask import request, redirect, url_for
from models import Task, TaskCategory, db

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

