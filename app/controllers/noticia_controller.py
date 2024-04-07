from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, storage
from ..models.not_model import Not
from flask_cors import CORS
from ..models.exceptions import userNotFound,CustomException,InvalidDataError,duplicateError
from werkzeug.utils import secure_filename

class notController:
    @classmethod
    def get(cls, idnoticias):
        try:
            noticia = Not.get(idnoticias)

            if noticia:
                serialized_product = {
                    "idnoticias": noticia.idnoticias,
                    "titulo": noticia.titulo,
                    "subtitulo": noticia.subtitulo,
                    "contenido": noticia.contenido,
                    "fecha":noticia.fecha,
                    "imagenes": noticia.urls_imagenes if hasattr(noticia, 'urls_imagenes') else []
                }

                return jsonify(serialized_product), 200
            else:
                return jsonify({'message': 'Noticia no encontrada'}), 404

        except Exception as e:
            print("Error al obtener el producto:", e)
            return jsonify({'message': 'Error en la solicitud'}), 500


    @classmethod
    def get_all(cls):
        try:
            noticias = Not.get_all()
            if noticias is not None:
                serialized_products = [noticia.serialize() for noticia in noticias]
                return jsonify(serialized_products), 200
            else:
                return jsonify({'message': 'No se pudieron obtener las noticias'}), 500
        except Exception as e:
            print("Error al obtener todos lAS NOTICIAS:", e)
            return jsonify({'message': 'Error en la solicitud'}), 500

    @classmethod
    def create(cls):
        try:
            # Obtener los datos del producto del cuerpo de la solicitud JSON
            data = request.json
            titulo = data['titulo']
            subtitulo = data['subtitulo']  # Cambiado el nombre del atributo
            contenido = data['contenido']
            fecha = data['fecha']
            url = data['url']  # Cambiado el nombre del atributo


            # Crear una nueva instancia del modelo de imagen con los datos proporcionados
            new_noticia = Not(**data)
            print(new_noticia)

            # Llamar al método de clase 'create' del modelo de imagen para crear la imagen en la base de datos
            if Not.create(new_noticia):
                return jsonify({'message': 'Noticia creada exitosamente'}), 201
            else:
                return jsonify({'message': 'Error al crear la noticia'}), 500

        except Exception as e:
            # Manejar cualquier error que ocurra durante el proceso de creación de la imagen
            return jsonify({'message': 'Error en la solicitud'}), 400
    @classmethod
    def update(cls, idnoticias):
        data = request.json
        valid_fields = ['titulo', 'subtitulo', 'contenido', 'fecha', 'url']
    
        if not data:
            return jsonify({'message': 'No se recibieron datos para actualizar'}), 400
    
        fields_to_update = {field: data.get(field) for field in data if field in valid_fields}
    
        if not fields_to_update:
            return jsonify({'message': 'No se proporcionaron campos válidos para actualizar'}), 400
    
        try:
            if 'url' in fields_to_update:
                # Procesar la actualización de la URL
                urls = fields_to_update.pop('url')  # Remover 'url' del diccionario
                Not.update_url(idnoticias, urls)  # Llamar al método para actualizar la URL
            # Actualizar otros campos
            response = Not.update(idnoticias, fields_to_update)
            return jsonify({'message': response}), 200
        except Exception as e:
            return jsonify({'message': str(e)}), 500
    
    

    @classmethod
    def delete(cls, idnoticias):
        try:
            # Eliminar todas las imágenes con el nombre del álbum (descripción) proporcionado
            if Not.delete(idnoticias):
                return jsonify({'message': 'Noticia eliminado exitosamente'}), 200
            else:
                raise userNotFound(idnoticias)  # Si no se encuentran imágenes para eliminar, lanzar la excepción userNotFound
        except Exception as e:
            print("Error al eliminar la noticia:", e)
            return jsonify ({'message': 'Error en la solicitud'}), 500   