from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import fields, validate
from models import db, Workout, Exercise, WorkoutExercise

class WorkoutExerciseSchema(SQLAlchemySchema):
    class Meta:
        model = WorkoutExercise
        load_instance = True
        sqla_session = db.session

    id = auto_field()
    reps = fields.Integer(
        required=True,
        validate=validate.Range(min=1, error="Reps must be at least 1.")
    )
    sets = fields.Integer(
        required=True,
        validate=validate.Range(min=1, error="Sets must be at least 1.")
    )
    duration_seconds = fields.Integer(
        required=True,
        validate=validate.Range(min=0, error="Duration must be 0 or greater.")
    )
    workout_id = auto_field(required=True)
    exercise_id = auto_field(required=True)
    exercise = fields.Nested(lambda: ExerciseSchema(only=("id", "name", "category")))


class ExerciseSchema(SQLAlchemySchema):
    class Meta:
        model = Exercise
        load_instance = True
        sqla_session = db.session

    id = auto_field()
    name = fields.String(
        required=True,
        validate=validate.Length(min=1, error="Name cannot be blank.")
    )
    category = fields.String(
        required=True,
        validate=validate.Length(min=1, error="Category cannot be blank.")
    )
    equipment_needed = fields.Boolean(required=True)
    workouts = fields.Nested(lambda: WorkoutSchema(only=("id", "date", "duration_minutes")), many=True)


class WorkoutSchema(SQLAlchemySchema):
    class Meta:
        model = Workout
        load_instance = True
        sqla_session = db.session

    id = auto_field()
    date = auto_field(required=True)
    duration_minutes = fields.Integer(
        required=True,
        validate=validate.Range(min=1, error="Duration must be positive.")
    )
    notes = fields.String(validate=validate.Length(max=300))

    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True)
    exercises = fields.Nested(lambda: ExerciseSchema(only=("id", "name", "category")), many=True)
