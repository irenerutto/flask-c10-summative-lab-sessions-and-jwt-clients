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

    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return {"error": "Username already exists."}, 409

    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    user = User(
        username=username,
        password_hash=password_hash
    )

    db.session.add(user)
    db.session.commit()

    session["user_id"] = user.id

    return {
        "id": user.id,
        "username": user.username
    }, 201

@app.post("/login")
def login():
    data = request.get_json()

    username = data.get("username", "").strip()
    password = data.get("password", "")

    user = User.query.filter_by(username=username).first()

    if not user:
        return {"error": "Invalid username or password."}, 401

    if not bcrypt.check_password_hash(user.password_hash, password):
        return {"error": "Invalid username or password."}, 401

    session["user_id"] = user.id

    return {
        "id": user.id,
        "username": user.username
    }, 200

@app.get("/check_session")
def check_session():
    user_id = session.get("user_id")

    if not user_id:
        return {"error": "Not authenticated."}, 401

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
    session.clear()

    return {
        "message": "Logged out successfully."
    }, 200


if __name__ == "__main__":
    app.run(port=5555, debug=True)
