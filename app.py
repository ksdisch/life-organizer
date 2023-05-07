from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from views.main_views import index
from views.daily_sched_views import daily_sched_builder, daily_sched_viewer, save_daily_schedule
from views.workout_views import workout_builder, workout_viewer
from views.goal_views import goals
from views.todo_views import todos
from views.item_views import items
from models import db

# Initialize Flask web app instance
app = Flask(__name__)
# Set the database URI to use a SQLite database named 'tasks.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///life-data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Home page
app.add_url_rule("/", view_func=index)

# Daily Schedule Builder
app.add_url_rule("/daily_sched_builder", view_func=daily_sched_builder)
# Processes and saves a new schedule once it is built
app.add_url_rule("/save_daily_schedule", view_func=save_daily_schedule, methods=['POST'])

# Daily Schedule Viewer
app.add_url_rule("/daily_sched_viewer", view_func=daily_sched_viewer, defaults={'date': None})
app.add_url_rule("/daily_sched_viewer/<date>", view_func=daily_sched_viewer)


# Workout Builder
app.add_url_rule("/workout_builder", view_func=workout_builder)

# Workout Viewer
app.add_url_rule("/workout_viewer", view_func=workout_viewer)

# Goals Page
app.add_url_rule("/goals", view_func=goals)

# To-do List Page
app.add_url_rule("/todos", view_func=todos)

# Items Page
app.add_url_rule("/items", view_func=items)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
