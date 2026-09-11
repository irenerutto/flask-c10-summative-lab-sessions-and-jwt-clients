# Personal Notes API

## Description

Personal Notes API is a Flask backend application that provides session-based authentication and a user-owned notes system.

Users can create an account, log in, check their session, log out, and manage their own notes. Each note belongs to the user who created it, and users cannot access or modify notes belonging to other users.

The API supports creating, reading, updating, deleting, and paginating notes.

## Features

* User registration and login
* Session-based authentication
* Secure password hashing with Flask-Bcrypt
* Session checking
* User logout
* User-owned notes
* Create, read, update, and delete notes
* Pagination for notes
* User ownership protection
* Model-level validation
* Database migrations with Flask-Migrate
* Seed data for development and testing
* SQLite for local development
* PostgreSQL for production
* Production deployment with Render and Gunicorn

## Technologies

* Python 3.8.13+
* Flask 2.2.2
* Flask-SQLAlchemy 3.0.3
* Flask-Migrate 4.0.0
* Flask-Bcrypt 1.0.1
* Marshmallow 3.20.1
* Flask-RESTful 0.3.9
* Gunicorn 20.1.0
* SQLite
* PostgreSQL
* Pipenv

## Project Structure

```text
flask-c10-summative-lab-sessions-and-jwt-clients/
│
├── client-with-jwt/
│   ├── README.md
│   ├── package.json
│   ├── package-lock.json
│   ├── public/
│   └── src/
│
├── client-with-sessions/
│   ├── README.md
│   ├── package.json
│   ├── package-lock.json
│   ├── public/
│   └── src/
│
├── server/
│   ├── app.py
│   ├── extensions.py
│   ├── models.py
│   ├── seed.py
│   ├── Pipfile
│   ├── Pipfile.lock
│   ├── .python-version
│   ├── .gitignore
│   └── migrations/
│       ├── versions/
│       ├── alembic.ini
│       ├── env.py
│       ├── script.py.mako
│       └── README
│
└── README.md
```

### Server Files

* `app.py` — Creates the Flask application, configures the database and session authentication, and defines the API routes.
* `models.py` — Defines the `User` and `Note` SQLAlchemy models, relationships, and model validation.
* `extensions.py` — Initializes SQLAlchemy, Flask-Migrate, and Flask-Bcrypt.
* `seed.py` — Creates sample users and notes for development and testing.
* `migrations/` — Contains Flask-Migrate and Alembic migration files.
* `Pipfile` — Lists the project's Python dependencies.
* `Pipfile.lock` — Locks dependency versions.
* `.python-version` — Specifies the Python version used by the project.
* `.gitignore` — Prevents environment files and generated files from being committed.

## Installation

### 1. Clone the Repository

```bash
git clone git@github.com:irenerutto/flask-c10-summative-lab-sessions-and-jwt-clients.git
cd flask-c10-summative-lab-sessions-and-jwt-clients/server
```

### 2. Install Dependencies

```bash
pipenv install
```

### 3. Activate the Virtual Environment

```bash
pipenv shell
```

## Environment Variables

The application uses environment variables for sensitive configuration.

Create a `.env` file inside the `server` directory:

```text
SECRET_KEY=your-development-secret-key
DATABASE_URL=your-database-url
```

The `.env` file should not be committed to Git.

For local development, SQLite is used when `DATABASE_URL` is not provided.

## Database Setup

The application uses Flask-Migrate and Alembic to manage database schema changes.

Apply the existing migrations with:

```bash
pipenv run flask db upgrade
```

To create a new migration after changing the models:

```bash
pipenv run flask db migrate -m "describe the change"
```

Then apply the migration:

```bash
pipenv run flask db upgrade
```

## Seed Data

The project includes a `seed.py` file that creates sample users and notes.

Run the seed script with:

```bash
pipenv run python seed.py
```

The seed script creates sample users with securely hashed passwords and associates sample notes with their respective users.

## Running the Application

From the `server` directory, run:

```bash
pipenv run python app.py
```

The application will run locally at:

```text
http://127.0.0.1:5555
```

## Authentication

This application uses session-based authentication.

Users must create an account and log in before accessing protected note routes.

Passwords are securely hashed using Flask-Bcrypt and are never stored as plain text.

The authenticated user's ID is stored in the Flask session. Note operations use this session information to ensure that users can only access and modify their own notes.

## API Endpoints

### Authentication Endpoints

| Method | Endpoint         | Description                                  |
| ------ | ---------------- | -------------------------------------------- |
| POST   | `/signup`        | Creates a new user account                   |
| POST   | `/login`         | Logs an existing user in                     |
| GET    | `/check_session` | Checks whether a user is currently logged in |
| POST   | `/logout`        | Logs the current user out                    |

### Notes Endpoints

| Method | Endpoint      | Description                                    |
| ------ | ------------- | ---------------------------------------------- |
| GET    | `/notes`      | Returns notes belonging to the logged-in user  |
| POST   | `/notes`      | Creates a new note for the logged-in user      |
| PATCH  | `/notes/<id>` | Updates a note belonging to the logged-in user |
| DELETE | `/notes/<id>` | Deletes a note belonging to the logged-in user |

All note endpoints require an authenticated session.

## Signup

### Request

```http
POST /signup
```

```json
{
    "username": "Irene",
    "password": "password123",
    "password_confirmation": "password123"
}
```

A successful signup creates the user and establishes an authenticated session.

## Login

### Request

```http
POST /login
```

```json
{
    "username": "Irene",
    "password": "password123"
}
```

A successful login establishes a session for the user.

## Check Session

### Request

```http
GET /check_session
```

This endpoint returns information about the currently authenticated user.

## Logout

### Request

```http
POST /logout
```

This clears the user's authentication session.

## Create a Note

### Request

```http
POST /notes
```

```json
{
    "title": "My first note",
    "content": "This is my personal note.",
    "category": "Personal"
}
```

The `user_id` does not need to be supplied by the client. It is obtained from the authenticated user's session.

## Get Notes

### Request

```http
GET /notes
```

The endpoint returns only notes belonging to the authenticated user.

## Notes Pagination

The `GET /notes` endpoint supports pagination using `page` and `per_page` query parameters.

Example:

```http
GET /notes?page=1&per_page=5
```

The response includes:

* Current page
* Number of notes per page
* Total number of notes
* Total number of pages
* Notes for the requested page

## Update a Note

### Request

```http
PATCH /notes/1
```

```json
{
    "title": "Updated note",
    "content": "This note has been updated.",
    "category": "Work"
}
```

Only the authenticated owner of the note can update it.

## Delete a Note

### Request

```http
DELETE /notes/1
```

Only the authenticated owner of the note can delete it.

## Security and Ownership

The application protects user-owned resources by associating every note with a user through a foreign key.

Users can only:

* View their own notes
* Create notes for themselves
* Update their own notes
* Delete their own notes

A user cannot access or modify another user's notes.

The application also prevents unauthenticated users from accessing protected note endpoints.

User passwords are hashed using Flask-Bcrypt before they are stored in the database.

## Validation

The `User` model validates usernames to ensure that they are not empty and contain at least three characters.

The `Note` model validates note titles to ensure that they are not empty.

The database also uses constraints such as required fields, unique usernames, primary keys, and foreign keys.

## Database

The application uses:

* SQLite for local development
* PostgreSQL for production

The production database connection is provided through the `DATABASE_URL` environment variable.

## Deployment

The API is deployed using Render.

### Production Services

* Render Web Service
* Render PostgreSQL
* Gunicorn

The Render web service runs the Flask application using:

```bash
gunicorn app:app
```

The production environment uses environment variables for the database connection and Flask session secret.

### Live API

```text
https://flask-notes-api-0q61.onrender.com
```

## Git and Version Control

The project uses Git for version control.

The completed application is maintained on the `main` branch of the GitHub repository.

Repository:

```text
git@github.com:irenerutto/flask-c10-summative-lab-sessions-and-jwt-clients.git
```
