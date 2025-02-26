import pytest
from app import app
from flask_jwt_extended import create_access_token

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["JWT_SECRET_KEY"] = "test_secret_key"  # Clave de prueba
    with app.test_client() as client:
        yield client

@pytest.fixture
def auth_header(client):
    # Crear un usuario y generar un token de autenticación para las pruebas
    client.post("/register", json={
        "username": "admin_user",
        "password": "password123",
        "role": "admin"
    })
    response = client.post("/login", json={
        "username": "admin_user",
        "password": "password123"
    })
    token = response.json["access_token"]
    return {"Authorization": f"Bearer {token}"}

# Prueba para el endpoint GET /tasks
def test_get_tasks(client, auth_header):
    response = client.get("/tasks", headers=auth_header)
    assert response.status_code == 200
    assert isinstance(response.json["tasks"], list)  # Verificar que las tareas sean una lista

# Prueba para el endpoint POST /tasks
def test_create_task(client, auth_header):
    data = {
        "title": "Nueva tarea de prueba",
        "description": "Descripción de prueba",
        "status": "pendiente"
    }
    response = client.post("/tasks", json=data, headers=auth_header)
    assert response.status_code == 201
    assert response.json["message"] == "Tarea creada exitosamente"

# Prueba para el endpoint GET /tasks/<id>
def test_get_task_by_id(client, auth_header):
    data = {
        "title": "Tarea específica",
        "description": "Prueba de detalle",
        "status": "pendiente"
    }
    post_response = client.post("/tasks", json=data, headers=auth_header)
    task_id = post_response.json["id"]

    response = client.get(f"/tasks/{task_id}", headers=auth_header)
    assert response.status_code == 200
    assert response.json["title"] == "Tarea específica"

# Prueba para el endpoint PUT /tasks/<id>
def test_update_task(client, auth_header):
    data = {
        "title": "Tarea para actualizar",
        "description": "Descripción original",
        "status": "pendiente"
    }
    post_response = client.post("/tasks", json=data, headers=auth_header)
    task_id = post_response.json["id"]

    update_data = {
        "title": "Tarea actualizada",
        "description": "Descripción actualizada",
        "status": "completada"
    }
    response = client.put(f"/tasks/{task_id}", json=update_data, headers=auth_header)
    assert response.status_code == 200
    assert response.json["message"] == "Tarea actualizada exitosamente"

# Prueba para el endpoint DELETE /tasks/<id>
def test_delete_task(client, auth_header):
    data = {
        "title": "Tarea para eliminar",
        "description": "Descripción de prueba",
        "status": "pendiente"
    }
    post_response = client.post("/tasks", json=data, headers=auth_header)
    task_id = post_response.json["id"]

    response = client.delete(f"/tasks/{task_id}", headers=auth_header)
    assert response.status_code == 200
    assert response.json["message"] == "Tarea eliminada exitosamente"

    # Verificar que la tarea ya no exista
    get_response = client.get(f"/tasks/{task_id}", headers=auth_header)
    assert get_response.status_code == 404
