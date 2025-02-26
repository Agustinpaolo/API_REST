from app import app

if __name__ == "__main__":
    from waitress import serve
    print("🚀 Servidor corriendo en http://127.0.0.1:5000")
    serve(app, host="0.0.0.0", port=5000)
