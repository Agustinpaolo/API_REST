# 📌 API REST - To-Do List

Esta es una API RESTful para gestionar tareas, desarrollada con **Flask**, utilizando **autenticación JWT**, control de acceso por **roles de usuario** (admin y usuario estándar), y conexión a base de datos **SQLite** o **PostgreSQL**.

## 🚀 Despliegue en producción

La aplicación está desplegada en [Render](https://render.com/) utilizando el servidor WSGI **Waitress**.

🔗 **Enlace a la API en producción**:  
https://api-rest-ll3v.onrender.com

---

## 📦 Tecnologías utilizadas

- Python 3
- Flask
- Flask-JWT-Extended
- SQLAlchemy
- Marshmallow
- dotenv
- Waitress
- Git + GitHub

---

## ⚙️ Instalación local

1. Clona el repositorio:

```bash
git clone https://github.com/tu_usuario/api_rest.git
cd api_rest

2. Crea y activa un entorno virtual:

python -m venv venv
venv\Scripts\activate  # En Windows
source venv/bin/activate  # En Linux/Mac

3. Instala las dependencias:

pip install -r requirements.txt

4. Crea un archivo .env con las siguientes variables:

SECRET_KEY=tu_clave_secreta
DATABASE_URL=sqlite:///tareas.db

5. Ejecuta el servidor en desarrollo:

python app.py

🔐 Autenticación y roles

La API utiliza tokens JWT. Los usuarios pueden tener dos tipos de rol:

admin: puede crear, editar y eliminar cualquier tarea.

user: solo puede ver, crear y modificar sus propias tareas.

🧪 Endpoints principales

| Método | Ruta          | Descripción                        |
| ------ | ------------- | ---------------------------------- |
| POST   | `/register`   | Registrar nuevo usuario            |
| POST   | `/login`      | Iniciar sesión y obtener token     |
| GET    | `/tasks`      | Ver todas las tareas               |
| POST   | `/tasks`      | Crear una nueva tarea              |
| GET    | `/tasks/<id>` | Ver una tarea específica           |
| PUT    | `/tasks/<id>` | Actualizar una tarea               |
| DELETE | `/tasks/<id>` | Eliminar una tarea (admin o dueño) |

✅ Pruebas

Para probar la API puedes usar herramientas como Postman o Insomnia. Asegúrate de incluir el token JWT en los headers:
Authorization: Bearer <token>

🌐 Despliegue en Render

1. Sube tu código a GitHub
2. Crea un nuevo servicio en Render (Web Service → Python)
3. Usa el siguiente comando de inicio:
python -m waitress --listen=0.0.0.0:$PORT app:app
4. Asegúrate de definir las variables de entorno SECRET_KEY y DATABASE_URL en Render.

🧠 Autor
Agustín - Desarrollador Python Junior.
Este proyecto forma parte de mi portafolio como desarrollador backend.
