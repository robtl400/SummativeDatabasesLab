#!/usr/bin/env python3

import sys
sys.path.append('server')
from app import app
from models import *
from datetime import date

with app.app_context():

    # Clear existing data
    WorkoutExercises.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    # Create exercises
    exercise1 = Exercise(name='Push-ups', category='Strength', equipment_needed=False)
    exercise2 = Exercise(name='Squats', category='Strength', equipment_needed=False)
    exercise3 = Exercise(name='Bench Press', category='Strength', equipment_needed=True)

    db.session.add_all([exercise1, exercise2, exercise3])
    db.session.commit()

    # Create workouts
    workout1 = Workout(date=date(2025, 1, 20), duration_minutes=45, notes='Morning workout')
    workout2 = Workout(date=date(2025, 1, 22), duration_minutes=60, notes='Leg day')

    db.session.add_all([workout1, workout2])
    db.session.commit()

    # Create workout exercises
    we1 = WorkoutExercises(workout_id=workout1.id, exercise_id=exercise1.id, reps=10, sets=3)
    we2 = WorkoutExercises(workout_id=workout1.id, exercise_id=exercise3.id, reps=8, sets=4)
    we3 = WorkoutExercises(workout_id=workout2.id, exercise_id=exercise2.id, reps=12, sets=3)

    db.session.add_all([we1, we2, we3])
    db.session.commit()

    print('Database seeded!')
