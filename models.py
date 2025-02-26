import sqlite3

# Función para conectar a la base de datos
def connect_db(testing=False):
    return sqlite3.connect(":memory:" if testing else "database.db")  # Soporte para pruebas

# Función para inicializar la base de datos
def init_db(testing=False):
    conn = connect_db(testing)
    cursor = conn.cursor()
    # Crear la tabla tasks si no existe
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT NOT NULL
    )
    """)
    # Crear la tabla users si no existe
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)
    # Crear índice en el campo status
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_status ON tasks(status)")
    conn.commit()
    conn.close()

# Función para obtener todas las tareas
def get_all_tasks():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, description, status FROM tasks")
        tasks = cursor.fetchall()
        return tasks
    except sqlite3.Error as e:
        print(f"Error al obtener tareas: {e}")
        return []
    finally:
        conn.close()

# Función para agregar una nueva tarea
def add_task(title, description, status):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)",
            (title, description, status)
        )
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error al agregar tarea: {e}")
    finally:
        conn.close()

# Función para actualizar una tarea
def update_task(task_id, title, description, status):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tasks SET title = ?, description = ?, status = ? WHERE id = ?",
            (title, description, status, task_id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            print(f"Tarea con ID {task_id} no encontrada.")
    except sqlite3.Error as e:
        print(f"Error al actualizar tarea: {e}")
    finally:
        conn.close()

# Función para eliminar una tarea
def delete_task_db(task_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        if cursor.rowcount == 0:
            print(f"Tarea con ID {task_id} no encontrada.")
    except sqlite3.Error as e:
        print(f"Error al eliminar tarea: {e}")
    finally:
        conn.close()

# Función para obtener una tarea específica por ID
def get_task_by_id(task_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, description, status FROM tasks WHERE id = ?", (task_id,))
        task = cursor.fetchone()
        return task
    except sqlite3.Error as e:
        print(f"Error al obtener tarea: {e}")
        return None
    finally:
        conn.close()
