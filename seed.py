#!/usr/bin/env python3

from app import app
from models import db, Workout, Exercise, WorkoutExercise
from datetime import date

with app.app_context():
    print("Clearing database...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    print("Seeding exercises...")
    pushup = Exercise(
        name="Push-Up",
        category="Chest",
        equipment_needed=False
    )
    squat = Exercise(
        name="Squat",
        category="Legs",
        equipment_needed=False
    )
    bench = Exercise(
        name="Bench Press",
        category="Chest",
        equipment_needed=True
    )
    db.session.add_all([pushup, squat, bench])
    db.session.commit()

    print("Seeding workouts...")
    workout1 = Workout(
        date=date(2025, 7, 20),
        duration_minutes=45,
        notes="Chest day workout"
    )
    workout2 = Workout(
        date=date(2025, 7, 22),
        duration_minutes=30,
        notes="Leg day"
    )
    db.session.add_all([workout1, workout2])
    db.session.commit()

    print("Adding exercises to workouts...")
    we1 = WorkoutExercise(
        workout=workout1,
        exercise=pushup,
        reps=15,
        sets=3,
        duration_seconds=60
    )
    we2 = WorkoutExercise(
        workout=workout1,
        exercise=bench,
        reps=10,
        sets=4,
        duration_seconds=120
    )
    we3 = WorkoutExercise(
        workout=workout2,
        exercise=squat,
        reps=12,
        sets=3,
        duration_seconds=90
    )
    db.session.add_all([we1, we2, we3])
    db.session.commit()

    print("✅ Database seeded successfully!")
