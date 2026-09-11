from app import app
from extensions import db, bcrypt
from models import User, Note


with app.app_context():
    print("Clearing existing data...")

    Note.query.delete()
    User.query.delete()

    print("Creating users...")

    user1 = User(
        username="Kimani",
        password_hash=bcrypt.generate_password_hash("password123").decode("utf-8")
    )

    user2 = User(
        username="Kossy",
        password_hash=bcrypt.generate_password_hash("password123").decode("utf-8")
    )

    db.session.add_all([user1, user2])
    db.session.commit()

    print("Creating notes...")

    note1 = Note(
        title="Welcome to Notes",
        content="This is Kimani's first note.",
        category="Personal",
        user_id=user1.id
    )

    note2 = Note(
        title="Work Tasks",
        content="Review the project requirements.",
        category="Work",
        user_id=user1.id
    )

    note3 = Note(
        title="Shopping List",
        content="Milk, bread, and vegetables.",
        category="Personal",
        user_id=user2.id
    )

    db.session.add_all([note1, note2, note3])
    db.session.commit()

    print("Seed data created successfully.")