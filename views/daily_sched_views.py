from flask import request, render_template, redirect, url_for, jsonify
from models import DailySchedule, Event, db
from datetime import datetime
import json
def daily_sched_builder():
    return render_template('daily_sched_builder.html')

def daily_sched_viewer(date=None):
    if date:
        # Convert the date string to a date object
        date = datetime.strptime(date, "%Y-%m-%d").date()
        daily_schedule = DailySchedule.query.filter_by(date=date).first()
        if daily_schedule:
            events = Event.query.filter_by(daily_schedule_id=daily_schedule.id).order_by(Event.start_time).all()
            for event in events:
                event.start_time = datetime.strptime(event.start_time, "%H:%M")
                event.end_time = datetime.strptime(event.end_time, "%H:%M")
        else:
            events = None
    else:
        events = None
    return render_template('daily_sched_viewer.html', events=events)


from flask import jsonify

def save_daily_schedule():
    # Extract the date from the form data
    date_str = request.form.get("schedule_date")
    if not date_str:
        return redirect(url_for('daily_sched_builder'))

    date = datetime.strptime(date_str, "%Y-%m-%d").date()

    daily_schedule = DailySchedule.query.filter_by(date=date).first()

    if not daily_schedule:
        daily_schedule = DailySchedule(date=date)
        db.session.add(daily_schedule)
        db.session.commit()

    # Extract all the events from the form data
    tasks = json.loads(request.form.get('task'))
    start_times_str = json.loads(request.form.get('start_time'))
    end_times_str = json.loads(request.form.get('end_time'))
    descriptions = json.loads(request.form.get('description'))

    for i in range(len(tasks)):
        start_time = datetime.strptime(start_times_str[i], "%H:%M").time().strftime('%H:%M')
        end_time = datetime.strptime(end_times_str[i], "%H:%M").time().strftime('%H:%M')

        event = Event(title=tasks[i], start_time=start_time, end_time=end_time, description=descriptions[i], daily_schedule_id=daily_schedule.id)

        db.session.add(event)
    db.session.commit()

    return redirect(url_for('daily_sched_viewer', date=date_str))
