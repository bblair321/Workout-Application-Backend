from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint
from datetime import date

db = SQLAlchemy()

class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=True)

    workout_exercises = db.relationship("WorkoutExercise", back_populates="workout", cascade="all, delete-orphan")

    # Many-to-many: Workout → Exercises (read-only)
    exercises = db.relationship(
        "Exercise",
        secondary="workout_exercises",
        back_populates="workouts",
        viewonly=True
    )

    __table_args__ = (
        CheckConstraint('duration_minutes > 0', name='check_duration_positive'),
    )

    @validates('duration_minutes')
    def validate_duration(self, key, value):
        if value <= 0:
            raise ValueError("Duration must be greater than zero")
        return value

    @validates('date')
    def validate_date(self, key, value):
        if value > date.today():
            raise ValueError("Workout date cannot be in the future")
        return value


class Exercise(db.Model):
    __tablename__ = 'exercises'

    VALID_CATEGORIES = {'Chest', 'Back', 'Legs', 'Arms', 'Shoulders', 'Core', 'Cardio', 'Flexibility'}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False)

    workout_exercises = db.relationship("WorkoutExercise", back_populates="exercise", cascade="all, delete-orphan")

    # Many-to-many: Exercise → Workouts (read-only)
    workouts = db.relationship(
        "Workout",
        secondary="workout_exercises",
        back_populates="exercises",
        viewonly=True
    )

    @validates('name')
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Exercise name cannot be empty")
        return value.strip()

    @validates('category')
    def validate_category(self, key, value):
        value = value.strip()
        if value not in self.VALID_CATEGORIES:
            raise ValueError(f"Category must be one of {self.VALID_CATEGORIES}")
        return value


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id', ondelete="CASCADE"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id', ondelete="CASCADE"), nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    duration_seconds = db.Column(db.Integer, nullable=False)

    workout = db.relationship("Workout", back_populates="workout_exercises")
    exercise = db.relationship("Exercise", back_populates="workout_exercises")

    __table_args__ = (
        db.UniqueConstraint('workout_id', 'exercise_id', name='_workout_exercise_uc'),
        CheckConstraint('reps >= 0', name='check_reps_nonnegative'),
        CheckConstraint('sets >= 0', name='check_sets_nonnegative'),
        CheckConstraint('duration_seconds >= 0', name='check_duration_seconds_nonnegative'),
    )

    @validates('reps', 'sets', 'duration_seconds')
    def validate_non_negative(self, key, value):
        if value < 0:
            raise ValueError(f"{key} must be zero or greater")
        return value
