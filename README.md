# REST API — To-Do List

A small but complete RESTful API for managing tasks, built with **Flask**, **JWT authentication**, **role-based access control** (admin and standard user), and **SQLAlchemy** with SQLite (local) or PostgreSQL (production).

> Live demo: https://api-rest-ll3v.onrender.com

---

## Features

- User registration and login with **JWT** tokens
- **RBAC**: `admin` can manage any task; `user` can only manage their own
- CRUD for tasks: create, list, get by id, update, delete
- Input/output validation with Marshmallow
- Production-ready WSGI entrypoint (Waitress) + `wsgi.py`
- Simple tests and DB bootstrap script

---

## Tech Stack

- Python 3.x, Flask
- Flask-JWT-Extended
- SQLAlchemy (+ Marshmallow)
- python-dotenv
- Waitress (WSGI)
- SQLite (dev) / PostgreSQL (prod)

---

## Project Structure

```
API_REST/
├─ app.py               # Flask app / routes and JWT setup
├─ models.py            # SQLAlchemy models and Marshmallow schemas
├─ init_database.py     # Quick DB seed/init script
├─ wsgi.py              # WSGI entrypoint for production
├─ requirements.txt
├─ database.db          # SQLite (dev) — ignored in production
├─ tests.py             # Basic tests / examples
└─ README.md
```

---

## Getting Started (Local)

### 1) Clone and enter the project

```bash
git clone https://github.com/Agustinpaolo/API_REST.git
cd API_REST
```

### 2) Create and activate a virtualenv

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python -m venv venv
source venv/bin/activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Environment variables

Create a `.env` file in the project root:

```bash
SECRET_KEY=change_this_secret
# SQLite (default/dev):
DATABASE_URL=sqlite:///database.db
# Or PostgreSQL (prod style):
# DATABASE_URL=postgresql+psycopg2://user:password@host:5432/dbname
```

### 5) Initialize the database (optional)

```bash
python init_database.py
```

### 6) Run in development

```bash
python app.py
# or, if app.py exposes app via Flask:
# flask --app app run --debug
```

The API will be available at: `http://127.0.0.1:5000/`

---

## Authentication & Roles

- Obtain a **JWT** by logging in.
- Send the token on protected endpoints using:

```
Authorization: Bearer <your_jwt_token>
```

**Roles**
- `admin`: full access to all users’ tasks
- `user`: can only view/update/delete their own tasks

---

## API Endpoints

### Auth

**Register**
```
POST /register
Content-Type: application/json

{
  "username": "alice",
  "password": "StrongPass123",
  "role": "user"   // or "admin" if allowed in your flow
}
```

**Login**
```
POST /login
Content-Type: application/json

{
  "username": "alice",
  "password": "StrongPass123"
}
```

**200 OK**
```json
{
  "access_token": "<JWT>"
}
```

### Tasks

> All task routes require `Authorization: Bearer <JWT>`

**List tasks**
```
GET /tasks
```

**Create task**
```
POST /tasks
Content-Type: application/json

{
  "title": "Buy milk",
  "description": "2 liters of whole milk",
  "done": false
}
```

**Get task by id**
```
GET /tasks/<id>
```

**Update task**
```
PUT /tasks/<id>
Content-Type: application/json

{
  "title": "Buy milk and eggs",
  "description": "2 L milk + 12 eggs",
  "done": true
}
```

**Delete task**
```
DELETE /tasks/<id>
```

- `admin`: can delete any task
- `user`: can delete only their own task

---

## Curl Examples

**Login**
```bash
curl -sX POST http://127.0.0.1:5000/login   -H 'Content-Type: application/json'   -d '{"username":"alice","password":"StrongPass123"}'
```

**Create a task**
```bash
TOKEN="eyJhbGciOi..." # set your token
curl -sX POST http://127.0.0.1:5000/tasks   -H "Authorization: Bearer $TOKEN"   -H 'Content-Type: application/json'   -d '{"title":"Buy milk","description":"2 L","done":false}'
```

**List tasks**
```bash
curl -s http://127.0.0.1:5000/tasks   -H "Authorization: Bearer $TOKEN"
```

---

## Running Tests

```bash
pytest -q      # if tests are written with pytest
# or
python tests.py
```

---

## Deployment (Render)

1. Push code to GitHub
2. In Render, create a **Web Service** (Python)
3. Set env vars `SECRET_KEY` and `DATABASE_URL`
4. Start command:

```bash
python -m waitress --listen=0.0.0.0:$PORT wsgi:app
# or:
python -m waitress --listen=0.0.0.0:$PORT app:app
```

> Ensure your `DATABASE_URL` uses PostgreSQL in production.

---

## Security Notes

- Keep `SECRET_KEY` private and **rotate** if leaked
- Use **HTTPS** in production
- Issue short-lived JWTs and consider refresh tokens
- Limit `admin` role assignment
