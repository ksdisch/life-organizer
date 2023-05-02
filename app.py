from flask import Flask, render_template, redirect, url_for, request
from models import db
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from views.main_views import index
from views.task_views import add_task, toggle_task
from views.grocery_views import add_grocery_item, toggle_grocery
from views.daily_scheduler_views import daily_schedule_builder, daily_schedule, save_daily_schedule
from views.workout_builder_views import workout_builder, save_workout, daily_workout

# Initialize Flask web app instance
app = Flask(__name__)
# Set the database URI to use a SQLite database named 'tasks.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'

db.init_app(app)
migrate = Migrate(app, db)  # Add this line

# Home page
app.add_url_rule("/", view_func=index)
app.add_url_rule("/add", view_func=add_task, methods=["POST"])
app.add_url_rule("/toggle-task/<int:task_id>", view_func=toggle_task, methods=["POST"])
app.add_url_rule("/add-grocery", view_func=add_grocery_item, methods=["POST"])
app.add_url_rule("/toggle-grocery/<int:grocery_id>", view_func=toggle_grocery, methods=["POST"])

# Daily schedule builder page
app.add_url_rule("/daily_schedule_builder", view_func=daily_schedule_builder)

# Saves the daily schedules
app.add_url_rule("/save_daily_schedule", view_func=save_daily_schedule, methods=['POST'])

# Daily schedules after user builds and submits them
app.add_url_rule("/daily_schedule/<date>", view_func=daily_schedule)

# Workout builder page
app.add_url_rule("/workout_builder", view_func=workout_builder)

# Saves the workout
app.add_url_rule("/save_workout", view_func=save_workout, methods=['POST'])

# Builds route for workout
app.add_url_rule("/daily_workout/<workout_date>", view_func=daily_workout)

if __name__ == '__main__':
    app.run(debug=True)
