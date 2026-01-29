Workout Tracker API

A Flask API for tracking workouts and exercises.

Installation

1. Install dependencies:
   pipenv install

2. Enter the virtual environment:
   pipenv shell

3. Initialize and migrate the database:
   cd server
   flask db init
   flask db migrate -m "initial"
   flask db upgrade head

4. Seed the database:
   cd ..
   python seed.py

Running the Server

cd server
python app.py

The server runs on http://localhost:5555

Endpoints

Workouts:
- GET /workouts - List all workouts
- GET /workouts/<id> - Get a workout with its exercises
- POST /workouts - Create a workout (body: date, duration_minutes, notes)
- DELETE /workouts/<id> - Delete a workout

Exercises:
- GET /exercises - List all exercises
- GET /exercises/<id> - Get an exercise with its workouts
- POST /exercises - Create an exercise (body: name, category, equipment_needed)
- DELETE /exercises/<id> - Delete an exercise

Workout Exercises:
- POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises - Add exercise to workout (body: reps, sets, duration_seconds)
