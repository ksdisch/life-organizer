from flask import request, render_template, redirect, url_for
from models import Task, TaskCategory, GroceryItem, GroceryCategory, DailySchedule, db
from datetime import datetime, timedelta

def daily_schedule_builder():
    tasks = Task.query.filter_by(completed=False).all()
    categories = TaskCategory.query.all()
    return render_template('daily_schedule_builder.html', tasks=tasks, categories=categories)

def daily_schedule(date):
    # Query the DailySchedule model for the given date
    schedule = DailySchedule.query.filter_by(date=date).first()

    # Check if a schedule exists for the given date
    if schedule:
        schedule_data = schedule.data
    else:
        schedule_data = {}  # Empty data if schedule does not exist

    # Pass the data to the template and render the daily schedule
    return render_template('daily_schedule.html', date=date, schedule_data=schedule_data, get_activity_for_time=get_activity_for_time, datetime=datetime, timedelta=timedelta)

from datetime import time, timedelta

def save_daily_schedule():
    schedule_date_str = request.form['schedule_date']

    if not schedule_date_str:
        return "Please select a date for this schedule to be logged."

    schedule_date = datetime.strptime(schedule_date_str, '%Y-%m-%d').date()
    schedule_data = {}

    num_activities = int(request.form['num_activities'])

    for i in range(num_activities):
        selected_option = request.form.get(f'activity_{i}', None)

        if not selected_option:
            continue

        start_time_str = request.form.get(f'start_time_{i}', '')
        end_time_str = request.form.get(f'end_time_{i}', '')

        if not start_time_str or not end_time_str:
            # Skip the activity if start_time or end_time is not provided
            continue

        start_time = datetime.strptime(start_time_str, '%H:%M').time()
        end_time = datetime.strptime(end_time_str, '%H:%M').time()

        # Convert start_time and end_time to 15-minute increments
        start_time = round_time(start_time, timedelta(minutes=15))
        end_time = round_time(end_time, timedelta(minutes=15))

        if selected_option == 'task':
            task_id = request.form.get(f'task_{i}', None)
            task = Task.query.get(task_id)
            task_value = task.title if task else None
        elif selected_option == 'category':
            category_id = request.form.get(f'category_{i}', None)
            category = TaskCategory.query.get(category_id)
            task_value = category.name if category else None
        else:
            task_value = request.form.get(f'custom_task_{i}', None)

        # Iterate through the 15-minute increments and assign the task value
        current_time = start_time
        while current_time < end_time:
            key = current_time.strftime('%H:%M')
            schedule_data[key] = task_value
            current_time += timedelta(minutes=15)

    # Assuming you have a Schedule model defined with appropriate fields/columns
    schedule = DailySchedule(date=schedule_date, data=schedule_data)

    db.session.add(schedule)  # Add the new Schedule instance to the database session.
    db.session.commit()  # Commit the database session, which will save the new schedule to the database.

    # Redirect the user to the daily schedule page for the corresponding date
    return redirect(url_for('daily_schedule', date=schedule_date))

def round_time(dt, time_delta):
    """Round datetime to the nearest time_delta increment."""
    seconds = (dt - dt.min).seconds
    rounding = (seconds + time_delta.seconds / 2) // time_delta.seconds * time_delta.seconds
    return dt + timedelta(0, rounding - seconds)


def get_activity_for_time(time, schedule_data):
    for activity in schedule_data:
        start_time = datetime.strptime(activity['start_time'], '%H:%M').time()
        end_time = datetime.strptime(activity['end_time'], '%H:%M').time()
        if start_time <= time < end_time:
            return activity
    return None

