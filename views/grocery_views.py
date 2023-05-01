from flask import request, redirect, url_for
from models import GroceryItem, GroceryCategory, db

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
