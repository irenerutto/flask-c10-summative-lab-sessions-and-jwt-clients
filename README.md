# Personal Notes API

---

## **Description**

Personal Notes API is a Flask backend application that provides session-based authentication and a user-owned notes system.

Users can create an account, log in, check their session, log out, and manage their own notes. Each note belongs to the user who created it, and users cannot access or modify notes belonging to other users.

The API supports creating, reading, updating, deleting, and paginating notes.

---

## **Installation**

### **1. Clone the Repository**

```bash
git clone git@github.com:irenerutto/flask-c10-summative-lab-sessions-and-jwt-clients.git
cd flask-c10-summative-lab-sessions-and-jwt-clients/server
```

### **2. Install Dependencies**

```bash
pipenv install
```

---

## **Database Setup**

Run the database migrations:

```bash
pipenv run flask db upgrade
```

Seed the database with sample users and notes:

```bash
pipenv run python seed.py
```

---

## **Running the Application**

From the `server` directory:

```bash
pipenv run python app.py
```

The API will run at:

**http://127.0.0.1:5555**

---

## **API Endpoints**

### **Authentication**

|  Method  | Endpoint         | Description                                     |
| :------: | ---------------- | ----------------------------------------------- |
| **POST** | `/signup`        | Creates a new user account and logs the user in |
| **POST** | `/login`         | Logs an existing user in                        |
|  **GET** | `/check_session` | Checks whether the current user is logged in    |
| **POST** | `/logout`        | Logs the current user out                       |

### **Notes**

|   Method   | Endpoint      | Description                                    |
| :--------: | ------------- | ---------------------------------------------- |
|   **GET**  | `/notes`      | Returns notes belonging to the logged-in user  |
|  **POST**  | `/notes`      | Creates a new note for the logged-in user      |
|  **PATCH** | `/notes/<id>` | Updates a note belonging to the logged-in user |
| **DELETE** | `/notes/<id>` | Deletes a note belonging to the logged-in user |

---

## **Notes Pagination**

The `GET /notes` endpoint supports pagination using `page` and `per_page` query parameters.

**Example:**

```text
GET /notes?page=1&per_page=5
```

The response includes:

* Current page
* Number of notes per page
* Total number of notes
* Total number of pages

---

## **Authentication and Security**

The API uses **Flask sessions** for authentication.

Passwords are securely hashed using **Flask-Bcrypt** before being stored in the database.

Protected routes require an authenticated session. Notes are associated with the logged-in user through the user's session, so users cannot access, update, or delete another user's notes.

The `user_id` is taken from the authenticated session rather than being supplied by the client when creating a note.

---

## **Example Requests**

### **Signup**

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

### **Login**

```http
POST /login
```

```json
{
    "username": "Irene",
    "password": "password123"
}
```

### **Create a Note**

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

### **Update a Note**

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

### **Delete a Note**

```http
DELETE /notes/1
```

---

## **Technologies**

* **Python 3.8.13+**
* **Flask 2.2.2**
* **Flask-SQLAlchemy 3.0.3**
* **Flask-Migrate 4.0.0**
* **Flask-Bcrypt 1.0.1**
* **Marshmallow 3.20.1**
* **Flask-RESTful 0.3.9**
* **SQLite**
* **Pipenv**

---

## **Repository**

**GitHub:** `git@github.com:irenerutto/flask-c10-summative-lab-sessions-and-jwt-clients.git`
