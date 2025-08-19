📌 API REST – To-Do List

API RESTful para gestionar tareas con Flask, JWT y control de acceso por roles. Persistencia en SQLite, documentación con Swagger (Flasgger) y despliegue en Render con Waitress.

Demo: https://api-rest-ll3v.onrender.com
Docs Swagger: /apidocs

🚀 Características

Autenticación con JWT (login/refresh, expiración de tokens).

Roles: admin (gestiona todo) y user (gestiona sus propias tareas).

CRUD de tareas (crear, listar, ver por ID, actualizar, eliminar).

Swagger UI con Flasgger.

Hash de contraseñas con Werkzeug.

Config por dotenv.

🧰 Tecnologías

Backend: Python, Flask, Flask-JWT-Extended

Docs: Flasgger (Swagger UI)

Persistencia: SQLite (stdlib sqlite3).

Seguridad: werkzeug.security (hash/salt)

Entorno/DevOps: python-dotenv, Git/GitHub

Producción: Waitress (Render)

🛠 Instalación local

git clone https://github.com/Agustinpaolo/API_REST.git
cd API_REST
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
pip install -r requirements.txt

Crear .env:

SECRET_KEY=tu_clave_secreta
DATABASE_URL=sqlite:///tareas.db

Ejecutar:

python app.py
# http://127.0.0.1:5000

🔐 Autenticación y roles

Enviar el token en cada request protegido:

Authorization: Bearer <token>

-admin: CRUD sobre cualquier tarea.
-user: CRUD sólo sobre sus tareas.

📑 Endpoints principales

| Método | Ruta          | Descripción          |
| -----: | ------------- | -------------------- |
|   POST | `/register`   | Registrar usuario    |
|   POST | `/login`      | Iniciar sesión (JWT) |
|    GET | `/tasks`      | Listar tareas        |
|   POST | `/tasks`      | Crear tarea          |
|    GET | `/tasks/<id>` | Ver tarea por ID     |
|    PUT | `/tasks/<id>` | Actualizar tarea     |
| DELETE | `/tasks/<id>` | Eliminar tarea       |

🌐 Despliegue en Render

-Servicio “Web Service → Python”.
-Comando:

python -m waitress --listen=0.0.0.0:$PORT app:app

-Variables de entorno: SECRET_KEY, DATABASE_URL.

✅ Pruebas manuales

Postman/Insomnia: incluir Authorization: Bearer <token> en requests a rutas protegidas.

👤 Autor

Agustín — Desarrollador Python Junior
GitHub: https://github.com/Agustinpaolo
