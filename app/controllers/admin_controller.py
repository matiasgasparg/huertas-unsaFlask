from flask import jsonify
from flask import Flask, jsonify, request,send_from_directory,current_app
import jwt
from ..models.admin_model import Admin

class adminController:
    @classmethod
    def login(cls):
        data = request.get_json()
        email = data.get('email', '')
        password = data.get('password', '')

        # Buscar el administrador por email y contraseña
        admin = next((admin for admin in Admin.get_all() if admin.email == email and admin.password == password), None)

        if admin:
            is_admin = 1 if admin.password == "adminunsa*" else 0  # Verificar si es un administrador
            # Generar el token JWT
            token = jwt.encode({
                'id_admin': admin.id_admin,
                'email': admin.email,
                'password': admin.password,
                'is_admin': is_admin  # Nuevo atributo para indicar si es administrador o no
            }, current_app.config['SECRET_KEY'], algorithm='HS256')

            response_data = {
                'message': 'Login successful',
                'id_usuario': admin.id_admin,
                'email': admin.email,
                'is_admin': is_admin,
                'token': token  # Devuelve el token JWT directamente
            }
            return jsonify(response_data), 200
        else:
            return jsonify({'message': 'Datos inválidos'}), 401
