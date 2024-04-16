from flask import Flask, request, jsonify
from ..models.huertas_model import Huerta
from flask_cors import CORS
from werkzeug.utils import secure_filename

class huertasController:
    @classmethod
    def get(cls, idhuertas):
        try:
            huerta = Huerta.get(idhuertas)

            if huerta:
                serialized_huerta = {
                    "idhuertas": huerta.idhuertas,
                    "titulo": huerta.titulo,
                    "direccion": huerta.direccion,
                    "descripcion": huerta.descripcion,
                    "url": huerta.url
                }

                return jsonify(serialized_huerta), 200
            else:
                return jsonify ({'message': 'Huerta no encontrada'}), 404

        except Exception as e:
            print("Error al obtener la huerta:", e)
            return jsonify({'message': 'Error en la solicitud'}), 500

    @classmethod
    def get_all(cls):
        try:
            huertas = Huerta.get_all()
            if huertas is not None:
                serialized_huertas = [huerta.serialize() for huerta in huertas]
                return jsonify(serialized_huertas), 200
            else:
                return jsonify({'message': 'No se pudieron obtener las huertas'}), 500
        except Exception as e:
            print("Error al obtener todas las huertas:", e)
            return jsonify({'message': 'Error en la solicitud'}), 500

    @classmethod
    def create(cls):
        try:
            data = request.json
            titulo = data['titulo']
            direccion = data['direccion']
            descripcion = data['descripcion']
            url = data['url']  # Cambiado el nombre del atributo
            new_huerta = Huerta(**data)

            if Huerta.create(new_huerta):
                return jsonify({'message': 'Huerta creada exitosamente'}), 201
            else:
                return jsonify({'message': 'Error al crear la huerta'}), 500

        except Exception as e:
            return jsonify({'message': 'Error en la solicitud'}), 400
    
    @classmethod
    def update(cls, idhuertas):
        data = request.json
        valid_fields = ['titulo', 'direccion', 'descripcion', 'url']

        if not data:
            return jsonify({'message': 'No se recibieron datos para actualizar'}), 400

        fields_to_update = {field: data.get(field) for field in data if field in valid_fields}

        if not fields_to_update:
            return jsonify({'message': 'No se proporcionaron campos válidos para actualizar'}), 400

        try:
            Huerta.update(idhuertas, fields_to_update)
            return jsonify({'message': 'Datos actualizados exitosamente'}), 200
        except Exception as e:
            return jsonify({'message': str(e)}), 500

    
    @classmethod
    def delete(cls, idhuertas):
        try:
            if Huerta.delete(idhuertas):
                return jsonify({'message': 'Huerta eliminada exitosamente'}), 200
            else:
                raise userNotFound(idhuertas)
        except Exception as e:
            print("Error al eliminar la huerta:", e)
            return jsonify({'message': 'Error en la solicitud'}), 500
