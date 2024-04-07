from app import init_app

if __name__ == "__main__":
    app = init_app()
    app.run(debug=True)  # Ejecutar la aplicación en modo debug