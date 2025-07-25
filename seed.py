#!/usr/bin/env python3

from app import app
from models import db

with app.app_context():
    db.drop_all()
    db.create_all()

    # Add seed data here in next steps
    # e.g.
    # exercise = Exercise(name="Squat", category="Legs", equipment_needed=True)
    # db.session.add(exercise)
    # db.session.commit()
