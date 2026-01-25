from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

# Define Models here

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50))
    equipment_needed = db.Column(db.Boolean, default=False)

    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name) < 2:
            raise ValueError('Exercise name must be at least 2 characters')
        return name


class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer)
    notes = db.Column(db.Text)

    @validates('duration_minutes')
    def validate_duration(self, key, duration):
        if duration is not None and duration < 1:
            raise ValueError('Duration must be at least 1 minute')
        return duration


class WorkoutExercises(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'))
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'))
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship('Workout', backref='workout_exercises')
    exercise = db.relationship('Exercise', backref='workout_exercises')
