from flask import request, render_template, redirect, url_for, jsonify
from models import Task, TaskCategory, GroceryItem, GroceryCategory, DailySchedule, Workout, Exercise, ExerciseCategory, db
from datetime import datetime, timedelta

def workout_builder():
    exercises = Exercise.query.all()
    categories = ExerciseCategory.query.all()

    return render_template('workout_builder.html', exercises=exercises, categories=categories)

def save_workout():
    workout_date_str = request.form['workout_date']

    if not workout_date_str:
        return "Please select a date for this workout to be logged."

    workout_date = datetime.strptime(workout_date_str, '%Y-%m-%d').date()

    # Extract exercise data
    exercises = request.form.getlist('exercise')
    exercise_categories = request.form.getlist('exercise_category')
    sets = request.form.getlist('sets')
    reps = request.form.getlist('reps')
    weights = request.form.getlist('weight')
    durations = request.form.getlist('duration')
    distances = request.form.getlist('distance')
    descriptions = request.form.getlist('description')

    workout_data = []

    for i in range(len(exercises)):
        exercise_data = {
            'title': exercises[i],
            'category_id': int(exercise_categories[i]) if exercise_categories[i] and exercise_categories[i] != 'new' else None,
            'sets': int(sets[i]) if sets[i] else None,
            'reps': int(reps[i]) if reps[i] else None,
            'weight': float(weights[i]) if weights[i] else None,
            'duration': durations[i] if durations[i] else None,
            'distance': float(distances[i]) if distances[i] else None,
            'description': descriptions[i]
        }
        workout_data.append(exercise_data)

        # Add new exercises to the exercises table
        if not Exercise.query.filter_by(title=exercises[i]).first():
            new_exercise = Exercise(
                title=exercises[i],
                category_id=exercise_data['category_id'],
                description=descriptions[i]
            )
            db.session.add(new_exercise)

    # Create a new Workout instance and set the date
    workout = Workout(workout_date=workout_date, workout_data=workout_data)
    db.session.add(workout)
    db.session.commit()

    return redirect(url_for('daily_workout', workout_date=workout_date_str))

# Add a new route and view function for the daily_workout page
def daily_workout(workout_date):
    workout_date_obj = datetime.strptime(workout_date, '%Y-%m-%d').date()
    workout = Workout.query.filter_by(workout_date=workout_date_obj).first()

    if not workout:
        return "No workout found for the given date", 404

    return render_template('daily_workout.html', workout=workout)





