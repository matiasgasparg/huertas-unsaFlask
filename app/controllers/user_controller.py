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
    def get(cls, id_usuario):
            user = User.get(id_usuario)  # Aquí se espera un ID de usuario, no un objeto User
            if user is not None:
                return user.serialize(), 200
            else:
                # Si no se encuentra el user, lanza la excepción userNotFound
                raise userNotFound(id_usuario)
    @classmethod
    def get_all(cls):
        """Get all users"""
        user_objects = User.get_all()
        users = []
        for user in user_objects:
            users.append(user.serialize())
        return users, 200

    @classmethod
    def create(cls):
        try:

            """Create a new User"""
            data = request.json
            name=data['name']
            lastname = data['lastname']
            email = data['email']
            telefono = data['telefono']

       

        
            new_user = User(**data)

            if User.create(new_user):
                return jsonify({'message': 'Usuario creado exitosamente'}), 201
            else:
                return jsonify({'message': 'Error al crear usuario'}), 500

        except Exception as e:
            return jsonify({'message': 'Error en la solicitud'}), 400    
    @classmethod
    def update(cls, id_usuario):
        """Update a User"""
        data = request.json
        field_to_update = data.get('field')  # Campo que se desea actualizar
        value = data.get('value')  # Nuevo valor para el campo
        valid_fields = ['username', 'email', 'name']  # Lista de campos válidos

        if field_to_update in valid_fields:
            if User.update(id_usuario, field_to_update, value):
                return jsonify({'message': f'{field_to_update.capitalize()} actualizado exitosamente'}), 200
            else:
                raise userNotFound(id_usuario)
        else:
            return jsonify({'message': 'Campo no válido para actualización'}), 400
    
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
        """Delete a User"""
        if not User.exists(id_usuario):
            raise userNotFound(id_usuario)

        User.delete(id_usuario)
        return {'message': 'User deleted successfully'}, 204
    @staticmethod
    def validate_input_data(data):
        """Validate input data"""
        if len(data.get('name', '')) < 3:
            raise InvalidDataError("El Nombre debe tener al menos 3 caracteres")
    
      

    
    @classmethod
    def logout(cls):
        session.pop('user_id', None)
        return {'message': 'Sesión cerrada exitosamente'}, 200