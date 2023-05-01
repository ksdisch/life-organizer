# This script initializes the database, then executes the script
# from app import app, db

# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()

# from app import app, db

# with app.app_context():
#     db.create_all()

from app import app, db, TaskCategory, GroceryCategory

with app.app_context():
    # Create tables
    db.create_all()

    # Add task categories
    task_categories = [
        'Job Search',
        'Self Care/Hygiene',
        'Interview Prep',
        'Personal Projects',
        'Upskill Activities',
        'Training/Workouts',
        'Research/Learning (Personal Interests)',
        'Other'
    ]

    for category in task_categories:
        task_category = TaskCategory(name=category)
        db.session.add(task_category)

    # Add grocery categories
    grocery_categories = [
        'Fruits',
        'Vegetables',
        'Dairy',
        'Meat',
        'Fish & Seafood',
        'Deli',
        'Condiments & Spices',
        'Snacks',
        'Bread & Bakery',
        'Beverages',
        'Pasta, Rice & Cereal',
        'Rice & Cereal',
        'Baking',
        'Frozen Foods',
        'Personal Care',
        'Health Care',
        'Household & Cleaning Supplies',
        'Pet Care',
        'Other'
    ]

    for category in grocery_categories:
        grocery_category = GroceryCategory(name=category)
        db.session.add(grocery_category)

    # Commit the changes
    db.session.commit()


# from app import db

# db.create_all()



# This allows me to easily run the script from the command line whenever I need to initialize or reset the database
# like I had to when I wanted to add categories to the lists which required updating of the database tables.

# This keeps your database initialization code separate from the main application code, making it easier 
# to manage and maintain.

# This script can be included as part of a deployment process, allowing you to automate database initialization
# when deploying your application to a server.