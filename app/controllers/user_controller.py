from ..models.user_model import User
from flask import Flask, jsonify, request,send_from_directory,current_app
from flask_cors import CORS
from decimal import Decimal
from ..models.exceptions import userNotFound,CustomException,InvalidDataError,duplicateError
from werkzeug.utils import secure_filename
import os
import jwt
from datetime import datetime, timedelta
from flask import jsonify
# app = Flask(__name__)

# CORS(app)  # Agregamos CORS a la aplicación
# app.config['UPLOAD_FOLDER'] = 'uploads'  # Carpeta donde se guardarán las imágenes

# users = [] 
SECRET_KEY = 'Pato'

class userController:
# Función para obtener un usuario por su ID de la base de datos
    @classmethod
    def get_asistencia(cls, idhuertas, id_practica):
        try:
            # Obtener la asistencia de todos los usuarios para una práctica específica y una huerta determinada
            users = User.get_asistencia(idhuertas, id_practica)
            
            if users:
                serialized_users = [user.serialize() for user in users]
                return jsonify(serialized_users), 200
            else:
                return jsonify({'message': 'No se encontraron usuarios o asistencia para la huerta y práctica especificadas'}), 404
        except Exception as e:
            print("Error al obtener los usuarios y su asistencia:", e)
            return jsonify({'message': 'Error en la solicitud'}), 500
    @classmethod
    def get(cls, idhuertas):
        try:
            users = User.get(idhuertas)  # Aquí se espera un ID de usuario, no un objeto User
            if users:
                serialized_users=[user.serialize()for user in users]
                return jsonify(serialized_users), 200
            else:
                return jsonify({'message': 'No se encontraron usuarios para la huerta'}), 404
        except Exception as e:
            print("Error al obtener los usuarios:", e)
            return jsonify({'message': 'Error en la solicitud'}), 500   

    @classmethod
    def create(cls,idhuertas):
        try:

            """Create a new User"""
            data = request.json
            print(data)
            name=data['name']
            lastname = data['lastname']
            email = data['email']
            telefono = data['telefono']
            new_user = User(**data)

            if User.create(new_user,idhuertas):
                return jsonify({'message': 'Usuario creado exitosamente'}), 201
            else:
                return jsonify({'message': 'Error al crear usuario'}), 500

        except Exception as e:
            return jsonify({'message': 'Error en la solicitud'}), 400    
    @staticmethod
    def asistencia(id_usuario, id_practica):
        try:
            data = request.json
            asistio = data['asistio']

            # Verificar si el usuario ya tiene una asistencia registrada en esta práctica
            if User.tiene_asistencia_registrada(id_usuario, id_practica):
                print("Aqui")
                return jsonify({'message': 'El usuario ya tiene una asistencia registrada en esta práctica'}), 400

            # El usuario no tiene una asistencia registrada, proceder con el registro
            if User.registrar_asistencia(id_usuario, id_practica, asistio):
                return jsonify({'message': 'Asistencia registrada exitosamente'}), 200
            else:
                return jsonify({'message': 'Error al registrar la asistencia'}), 500
        except Exception as e:
            print("Error al registrar la asistencia:", e)
            return jsonify({'message': 'Error en la solicitud'}), 500

    @classmethod
    def login(cls):
        data = request.get_json()
        email = data.get('email', '')
        password = data.get('password', '')
        admin = data.get('admin', '')

        user = next((user for user in User.get_all() if (user.email == email or user.username == username) and user.password == password), None)

        if user:
            admin = 1 if user.password == "adminunsa*" else 0

            # Generar el token JWT
            token = jwt.encode({
                'id_usuario': user.id_usuario,
                'username': user.username,
                'admin': admin
            }, current_app.config['SECRET_KEY'], algorithm='HS256')


            
            response_data = {
                'message': 'Login successful',
                'id_usuario': user.id_usuario,
                'username': user.username,
                'admin': admin,
                'token': token  # Devuelve el token JWT directamente
            }
            print(response_data)
            return jsonify(response_data), 200
        else:
            return jsonify({'message': 'Datos inválidos'}), 401
    @classmethod
    def delete(cls,id_usuario):
        try:
            # Eliminar la imagen de la tabla imagen
            if User.delete(id_usuario):
                # Eliminar la relación en la tabla huertas_has_imagen
                if User.deleteRelationByImageId(id_usuario):
                    return jsonify({'message': 'Usuario eliminada exitosamente'}), 200
                else:
                    raise userNotFound(f"La relación huertas_has_usuario no se encontró para usuario {id_usuario} e idhuerta {idhuerta}")
            else:
                raise userNotFound(f"La Huerta no se encontró para usuario {id_usuario}")
        except Exception as e:
            print("Error al eliminar la imagen:", e)
            return jsonify({'message': 'Error en la solicitud'}), 500

    @staticmethod
    def validate_input_data(data):
        """Validate input data"""
        if len(data.get('name', '')) < 3:
            raise InvalidDataError("El Nombre debe tener al menos 3 caracteres")
      

    
    @classmethod
    def logout(cls):
        session.pop('user_id', None)
        return {'message': 'Sesión cerrada exitosamente'}, 200