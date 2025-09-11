# REST API – Task Manager

A RESTful API built with Flask to manage tasks. It includes JWT-based authentication, role-based access control, task CRUD operations, and Swagger documentation.

## Features
- **User registration** with role assignment (admin or user).
- **Login** to obtain JWT tokens.
- **Role-based access control**:  
  - Admin can create, update, delete, and view tasks.
  - Regular users can only list tasks.
- **CRUD operations for tasks**:
  - Create, read, update, delete.
  - Search, filter, and paginate tasks.
- **Swagger UI** at `/apidocs` for easy API exploration.
- **Health check endpoint**.

---

## Project Structure
```
project/
├── app.py           # Main Flask application
├── models.py        # Database functions
├── .env             # Environment variables
```

---

## Environment Variables
The application uses the following variables from the `.env` file:
- `SECRET_KEY` – Flask secret key.
- `JWT_SECRET_KEY` – Key for JWT token generation.

---

## Installation
```bash
# Clone the repository
git clone <repo_url>

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

---

## Endpoints

### **Authentication**
#### `POST /register`
Register a new user.

**Body:**
```json
{
  "username": "new_user",
  "password": "mypassword",
  "role": "admin"
}
```

**Responses:**
- `201` – User successfully registered.
- `400` – Missing fields or username already exists.

---

#### `POST /login`
Authenticate and obtain a JWT token.

**Body:**
```json
{
  "username": "new_user",
  "password": "mypassword"
}
```

**Responses:**
- `200` – Token generated successfully.
- `401` – Invalid credentials.

---

### **Tasks**
> **Note:** Admin role required for creating, updating, deleting, and viewing tasks by ID.

#### `GET /tasks`
Get all tasks with pagination, search, and filtering.

**Query Parameters:**
- `page` *(int)* – Page number. Default: 1  
- `per_page` *(int)* – Results per page. Default: 5  
- `search` *(string)* – Search text for title or description.  
- `status` *(string)* – Filter by task status.

**Response:**
```json
{
  "total": 10,
  "page": 1,
  "per_page": 5,
  "tasks": [
    {
      "id": 1,
      "title": "Task Title",
      "description": "Task Description",
      "status": "pending"
    }
  ]
}
```

---

#### `POST /tasks` *(Admin only)*
Create a new task.

**Body:**
```json
{
  "title": "New Task",
  "description": "Task description",
  "status": "pending"
}
```

**Responses:**
- `201` – Task successfully created.
- `400` – Missing required fields.

---

#### `GET /tasks/<task_id>` *(Admin only)*
Get a task by its ID.

**Response:**
```json
{
  "id": 1,
  "title": "Task Title",
  "description": "Task Description",
  "status": "pending"
}
```

- `404` – Task not found.

---

#### `PUT /tasks/<task_id>` *(Admin only)*
Update an existing task.

**Body:**
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "status": "completed"
}
```

**Responses:**
- `200` – Task updated successfully.
- `400` – Missing required fields.
- `404` – Task not found.

---

#### `DELETE /tasks/<task_id>` *(Admin only)*
Delete a task by ID.

**Responses:**
- `200` – Task successfully deleted.
- `404` – Task not found.

---

### **Miscellaneous**
#### `GET /health`
Health check for the API.
```json
{
  "status": "ok"
}
```

#### `GET /`
Welcome endpoint.  
```json
{
  "message": "Welcome to the REST API",
  "docs": "/apidocs"
}
```

---

## Authentication
This API uses **JWT tokens**:
- Include the token in the header:
  ```
  Authorization: Bearer <your_token>
  ```
- Tokens are generated at the `/login` endpoint.

---

## Swagger UI
Interactive documentation is available at:
```
http://<host>:5000/apidocs
```

---

## Error Handling
Common error responses:
- `400` – Bad request (missing or invalid data).
- `401` – Unauthorized (missing or invalid token).
- `403` – Forbidden (insufficient role permissions).
- `404` – Resource not found.
- `422` – Invalid or expired token.
- `500` – Internal server error.
