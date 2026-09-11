import os

from flask import Flask, request, session

from extensions import db, migrate, bcrypt


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "notes-api-development-key"
)


db.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)


from models import User, Note


@app.route("/")
def home():
    return {"message": "Personal Notes API is running!"}


@app.post("/signup")
def signup():
    # Get the data sent by the user.
    data = request.get_json()

    username = data.get("username", "").strip()
    password = data.get("password", "")
    password_confirmation = data.get("password_confirmation", "")

    if not username:
        return {"error": "Username is required."}, 400

    if len(username) < 3:
        return {"error": "Username must be at least 3 characters."}, 400

    if not password:
        return {"error": "Password is required."}, 400

    if len(password) < 6:
        return {"error": "Password must be at least 6 characters."}, 400

    if password != password_confirmation:
        return {"error": "Passwords do not match."}, 400
    # Check whether this username is already registered.
    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return {"error": "Username already exists."}, 409

    # Hash the password before saving it to the database.
    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    user = User(
        username=username,
        password_hash=password_hash
    )
    # Save the new user to the database.
    db.session.add(user)
    db.session.commit()
    # Store the logged-in user's ID in the session for authenticated requests.
    session["user_id"] = user.id

    return {
        "id": user.id,
        "username": user.username
    }, 201

@app.post("/login")
def login():
    # Get the login details sent by the user.
    data = request.get_json()

    username = data.get("username", "").strip()
    password = data.get("password", "")
    # Find the user with the username provided.
    user = User.query.filter_by(username=username).first()

    if not user:
        return {"error": "Invalid username or password."}, 401
    # Compare the entered password with the stored password hash.
    if not bcrypt.check_password_hash(user.password_hash, password):
        return {"error": "Invalid username or password."}, 401
    # Store the user's ID in the session after successful login.
    session["user_id"] = user.id

    return {
        "id": user.id,
        "username": user.username
    }, 200

@app.get("/check_session")
def check_session():
    # Get the logged-in user's ID from the session.
    user_id = session.get("user_id")

    if not user_id:
        return {"error": "Not authenticated."}, 401
    # Find the user stored in the session.
    user = User.query.get(user_id)

    if not user:
        session.clear()
        return {"error": "Not authenticated."}, 401

    return {
        "id": user.id,
        "username": user.username
    }, 200

@app.post("/logout")
def logout():
    # Remove the user's login information from the session.
    session.clear()

    return {
        "message": "Logged out successfully."
    }, 200

@app.get("/notes")
def get_notes():
    user_id = session.get("user_id")

    if not user_id:
        return {"error": "Not authenticated."}, 401
    # Get the requested page number and number of notes per page.
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)

    if page < 1:
        page = 1

    if per_page < 1:
        per_page = 5
    # Only return notes belonging to the user in the current session.
    notes = Note.query.filter_by(user_id=user_id).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return {
        "notes": [
            {
                "id": note.id,
                "title": note.title,
                "content": note.content,
                "category": note.category
            }
            for note in notes.items
        ],
        "pagination": {
            "page": notes.page,
            "per_page": notes.per_page,
            "total": notes.total,
            "pages": notes.pages
        }
    }, 200

@app.post("/notes")
def create_note():
    # Get the logged-in user's ID from the session.
    user_id = session.get("user_id")

    if not user_id:
        return {"error": "Not authenticated."}, 401
    # Get the note details sent by the user.
    data = request.get_json()

    title = data.get("title", "").strip()
    content = data.get("content", "").strip()
    category = data.get("category", "General").strip()

    if not title:
        return {"error": "Title is required."}, 400

    if not content:
        return {"error": "Content is required."}, 400
    # Create the note and connect it to the logged-in user.
    note = Note(
        title=title,
        content=content,
        category=category,
        user_id=user_id
    )
    # Save the new note to the database.
    db.session.add(note)
    db.session.commit()

    return {
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "category": note.category
    }, 201

@app.patch("/notes/<int:id>")
def update_note(id):
    # Get the logged-in user's ID from the session.
    user_id = session.get("user_id")

    if not user_id:
        return {"error": "Not authenticated."}, 401
    # Find the note only if it belongs to the logged-in user.
    note = Note.query.filter_by(id=id, user_id=user_id).first()

    if not note:
        return {"error": "Note not found."}, 404
    # Get the updated note details from the request.
    data = request.get_json()

    if "title" in data:
        title = data["title"].strip()

        if not title:
            return {"error": "Title cannot be empty."}, 400

        note.title = title

    if "content" in data:
        content = data["content"].strip()

        if not content:
            return {"error": "Content cannot be empty."}, 400

        note.content = content

    if "category" in data:
        category = data["category"].strip()

        if not category:
            return {"error": "Category cannot be empty."}, 400

        note.category = category
    # Save the changes to the database.
    db.session.commit()

    return {
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "category": note.category
    }, 200

@app.delete("/notes/<int:id>")
def delete_note(id):
    # Get the logged-in user's ID from the session.
    user_id = session.get("user_id")

    if not user_id:
        return {"error": "Not authenticated."}, 401
    # Find the note only if it belongs to the logged-in user.
    note = Note.query.filter_by(id=id, user_id=user_id).first()

    if not note:
        return {"error": "Note not found."}, 404
    # Delete the note from the database.
    db.session.delete(note)
    db.session.commit()

    return {
        "message": "Note deleted successfully."
    }, 200

if __name__ == "__main__":
    app.run(port=5555, debug=True)
