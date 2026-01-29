from flask import Flask, make_response, request
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from marshmallow import fields, validate

import sys
sys.path.append('..')
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)
ma = Marshmallow(app)


# Schemas
class ExerciseSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Exercise

    id = ma.auto_field()
    name = fields.String(required=True, validate=validate.Length(min=2))
    category = ma.auto_field()
    equipment_needed = ma.auto_field()


class WorkoutSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Workout

    id = ma.auto_field()
    date = ma.auto_field()
    duration_minutes = fields.Integer(validate=validate.Range(min=1))
    notes = ma.auto_field()


class WorkoutExercisesSchema(ma.SQLAlchemySchema):
    class Meta:
        model = WorkoutExercises

    id = ma.auto_field()
    workout_id = ma.auto_field()
    exercise_id = ma.auto_field()
    reps = ma.auto_field()
    sets = ma.auto_field()
    duration_seconds = ma.auto_field()
    exercise = fields.Nested(ExerciseSchema)


exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_exercises_schema = WorkoutExercisesSchema()


# Workout Routes
@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return make_response(workouts_schema.dump(workouts), 200)


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return make_response({'error': 'Workout not found'}, 404)
    result = workout_schema.dump(workout)
    result['exercises'] = WorkoutExercisesSchema(many=True).dump(workout.workout_exercises)
    return make_response(result, 200)


@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()
    errors = workout_schema.validate(data)
    if errors:
        return make_response({'errors': errors}, 400)
    workout = Workout(
        date=data.get('date'),
        duration_minutes=data.get('duration_minutes'),
        notes=data.get('notes')
    )
    db.session.add(workout)
    db.session.commit()
    return make_response(workout_schema.dump(workout), 201)


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return make_response({'error': 'Workout not found'}, 404)
    WorkoutExercises.query.filter_by(workout_id=id).delete()
    db.session.delete(workout)
    db.session.commit()
    return make_response({'message': 'Workout deleted'}, 200)


# Exercise Routes
@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return make_response(exercises_schema.dump(exercises), 200)


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return make_response({'error': 'Exercise not found'}, 404)
    result = exercise_schema.dump(exercise)
    result['workouts'] = WorkoutExercisesSchema(many=True).dump(exercise.workout_exercises)
    return make_response(result, 200)


@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()
    errors = exercise_schema.validate(data)
    if errors:
        return make_response({'errors': errors}, 400)
    try:
        exercise = Exercise(
            name=data.get('name'),
            category=data.get('category'),
            equipment_needed=data.get('equipment_needed', False)
        )
        db.session.add(exercise)
        db.session.commit()
        return make_response(exercise_schema.dump(exercise), 201)
    except ValueError as e:
        return make_response({'error': str(e)}, 400)


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return make_response({'error': 'Exercise not found'}, 404)
    WorkoutExercises.query.filter_by(exercise_id=id).delete()
    db.session.delete(exercise)
    db.session.commit()
    return make_response({'message': 'Exercise deleted'}, 200)


# WorkoutExercises Route
@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get(workout_id)
    exercise = Exercise.query.get(exercise_id)
    if not workout:
        return make_response({'error': 'Workout not found'}, 404)
    if not exercise:
        return make_response({'error': 'Exercise not found'}, 404)
    data = request.get_json()
    workout_exercise = WorkoutExercises(
        workout_id=workout_id,
        exercise_id=exercise_id,
        reps=data.get('reps'),
        sets=data.get('sets'),
        duration_seconds=data.get('duration_seconds')
    )
    db.session.add(workout_exercise)
    db.session.commit()
    return make_response(workout_exercises_schema.dump(workout_exercise), 201)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
