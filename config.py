from dotenv import dotenv_values

# Cargar las variables de entorno desde el archivo .env
config = dotenv_values(".env")

class Config:
    SECRET_KEY = config['SECRET_KEY']  # Utiliza la clave secreta del archivo .env
    DEBUG = False

    DATABASE_USERNAME = config['DATABASE_USERNAME']
    DATABASE_PASSWORD = config['DATABASE_PASSWORD']
    DATABASE_HOST = config['DATABASE_HOST']
    DATABASE_PORT = config['DATABASE_PORT']

    DATABASE_NAME = config['DATABASE_NAME']
    TEMPLATE_FOLDER = "templates/"
    STATIC_FOLDER = "static_folder/"       
    