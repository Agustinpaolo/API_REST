from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from flasgger import Swagger
from models import init_db, get_all_tasks, get_task_by_id, add_task, update_task, delete_task_db, connect_db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, get_jwt, jwt_required
from functools import wraps
import sqlite3

# Cargar las variables del .env
load_dotenv()

# Inicializar la aplicación Flask
app = Flask(__name__)

# Usar las variables de entorno
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "valor_por_defecto")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "tu_clave_secreta")  # Se obtiene del .env si está configurado

# Configurar Swagger
swagger = Swagger(app)

# Inicializar la base de datos
init_db()

# Configurar JWT
app.config["JWT_SECRET_KEY"] = "tu_clave_secreta"  # Cambia esto por una clave segura
jwt = JWTManager(app)

# Manejar errores de tokens inválidos
@jwt.invalid_token_loader
def invalid_token_callback(reason):
    return jsonify({
        "error": "Token inválido",
        "message": "El token proporcionado no es válido o tiene un formato incorrecto"
    }), 401

@jwt.unauthorized_loader
def unauthorized_callback(reason):
    return jsonify({"error": "No se proporcionó un token válido", "message": reason}), 401

# Middleware para manejar errores globales
@app.errorhandler(404)
def handle_404_error(e):
    return jsonify({"error": "Recurso no encontrado"}), 404

@app.errorhandler(400)
def handle_400_error(e):
    return jsonify({"error": "Solicitud inválida"}), 400

@app.errorhandler(422)
def handle_invalid_token(e):
    return jsonify({"error": "El token proporcionado es inválido o ha expirado"}), 422

@app.errorhandler(500)
def handle_500_error(e):
    return jsonify({"error": "Error interno del servidor"}), 500

# Decorador para verificar roles
def role_required(role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            if claims.get("role") != role:
                return jsonify({"error": f"Acceso denegado: Se requiere rol '{role}'"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator

@app.route("/register", methods=["POST"])
def register():
    """
    Registrar un nuevo usuario con un rol
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              example: "nuevo_usuario"
            password:
              type: string
              example: "contraseña123"
            role:
              type: string
              example: "admin"
    responses:
      201:
        description: Usuario registrado exitosamente
      400:
        description: Error en la solicitud (falta de datos obligatorios o usuario ya existente)
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "user")

    # Validar campos obligatorios
    if not username or not password:
        return jsonify({"error": "Los campos 'username' y 'password' son obligatorios"}), 400

    # Hashear la contraseña
    hashed_password = generate_password_hash(password)

    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, hashed_password, role)
        )
        conn.commit()
        return jsonify({"message": "Usuario registrado exitosamente"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "El nombre de usuario ya existe"}), 400
    except Exception as e:
        return jsonify({"error": f"Ocurrió un error al registrar el usuario: {e}"}), 500
    finally:
        # Asegurarse de cerrar la conexión a la base de datos
        if conn:
            conn.close()

@app.route("/login", methods=["POST"])
def login():
    """
    Iniciar sesión y obtener un token JWT
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              example: "nuevo_usuario"
            password:
              type: string
              example: "contraseña123"
    responses:
      200:
        description: Token generado exitosamente
      401:
        description: Credenciales inválidas
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Los campos 'username' y 'password' son obligatorios"}), 400

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT password, role FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if not user or not check_password_hash(user[0], password):
        return jsonify({"error": "Credenciales inválidas"}), 401

    access_token = create_access_token(identity=username, additional_claims={"role": user[1]})
    return jsonify({"access_token": access_token}), 200

@app.route("/tasks", methods=["GET"])
@jwt_required()
def get_tasks():
    """
    Obtener todas las tareas con paginación, búsqueda y filtrado
    ---
    parameters:
      - in: query
        name: page
        type: integer
        required: false
        description: Número de la página.
        example: 1
      - in: query
        name: per_page
        type: integer
        required: false
        description: Número de resultados por página.
        example: 5
      - in: query
        name: search
        type: string
        required: false
        description: Texto para buscar en el título o descripción.
        example: "reunión"
      - in: query
        name: status
        type: string
        required: false
        description: Filtrar por estado (pendiente o completada).
        example: "pendiente"
    responses:
      200:
        description: Lista de tareas con paginación, búsqueda y filtrado
    """
    # Obtener parámetros de la solicitud
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 5))
    search = request.args.get("search", "").lower()
    status = request.args.get("status", "").lower()

    # Obtener todas las tareas
    tasks = get_all_tasks()

    # Filtrar por búsqueda en título o descripción
    if search:
        tasks = [task for task in tasks if search in task[1].lower() or search in task[2].lower()]

    # Filtrar por estado
    if status:
        tasks = [task for task in tasks if task[3].lower() == status]

    # Implementar paginación
    total_tasks = len(tasks)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_tasks = tasks[start:end]

    # Crear respuesta con paginación
    return jsonify({
        "total": total_tasks,
        "page": page,
        "per_page": per_page,
        "tasks": [{
            "id": task[0],
            "title": task[1],
            "description": task[2],
            "status": task[3]
        } for task in paginated_tasks]
    })

@app.route("/tasks", methods=["POST"])
@jwt_required()
@role_required("admin")
def create_task():
    """
    Crear una nueva tarea
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              example: "Nueva tarea"
            description:
              type: string
              example: "Descripción de la nueva tarea"
            status:
              type: string
              example: "pendiente"
    responses:
      201:
        description: Tarea creada exitosamente
      400:
        description: Error en la solicitud (falta de datos obligatorios)
    """
    data = request.get_json()
    title = data.get("title")
    description = data.get("description", "")
    status = data.get("status", "pendiente")

    if not title:
        return jsonify({"error": "El campo 'title' es obligatorio"}), 400

    add_task(title, description, status)
    return jsonify({"message": "Tarea creada exitosamente"}), 201

@app.route("/tasks/<int:task_id>", methods=["PUT"])
@jwt_required()
@role_required("admin")
def update_task_endpoint(task_id):
    """
    Actualizar una tarea existente
    ---
    parameters:
      - in: path
        name: task_id
        required: true
        type: integer
        description: ID de la tarea a actualizar
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              example: "Título actualizado"
            description:
              type: string
              example: "Descripción actualizada"
            status:
              type: string
              example: "completada"
    responses:
      200:
        description: Tarea actualizada exitosamente
      400:
        description: Error en la solicitud (falta de datos obligatorios)
      404:
        description: Tarea no encontrada
    """
    task = get_task_by_id(task_id)
    if not task:
        return jsonify({"error": "Tarea no encontrada"}), 404

    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    status = data.get("status")

    if not title or not status:
        return jsonify({"error": "Los campos 'title' y 'status' son obligatorios"}), 400

    update_task(task_id, title, description, status)
    return jsonify({"message": "Tarea actualizada exitosamente"}), 200

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
@jwt_required()
@role_required("admin")
def delete_task(task_id):
    """
    Eliminar una tarea
    ---
    parameters:
      - in: path
        name: task_id
        required: true
        type: integer
        description: ID de la tarea a eliminar
    responses:
      200:
        description: Tarea eliminada exitosamente
      404:
        description: Tarea no encontrada
    """
    task = get_task_by_id(task_id)
    if not task:
        return jsonify({"error": "Tarea no encontrada"}), 404

    delete_task_db(task_id)
    return jsonify({"message": "Tarea eliminada exitosamente"}), 200

@app.route("/tasks/<int:task_id>", methods=["GET"])
@jwt_required()
@role_required("admin")
def get_task_by_id_endpoint(task_id):
    """
    Obtener una tarea por ID
    ---
    parameters:
      - in: path
        name: task_id
        required: true
        type: integer
        description: ID de la tarea a obtener
    responses:
      200:
        description: Tarea encontrada
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            title:
              type: string
              example: "Título de la tarea"
            description:
              type: string
              example: "Descripción de la tarea"
            status:
              type: string
              example: "pendiente"
      404:
        description: Tarea no encontrada
    """
    task = get_task_by_id(task_id)  # Usa la función `get_task_by_id` de tu módulo `models`.
    if not task:
        return jsonify({"error": "Tarea no encontrada"}), 404

    return jsonify({
        "id": task[0],
        "title": task[1],
        "description": task[2],
        "status": task[3]
    }), 200

@app.route("/health", methods=["GET"])
def home():
    return jsonify({
        "message": "Bienvenido a la API REST",
        "docs": "/apidocs"
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
