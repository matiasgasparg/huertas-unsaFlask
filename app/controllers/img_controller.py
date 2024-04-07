from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, storage
from ..models.img_model import Img
from flask_cors import CORS
from ..models.exceptions import userNotFound,CustomException,InvalidDataError,duplicateError
from werkzeug.utils import secure_filename

class imgController:
    @classmethod
    def upload_image(cls):
        if 'image' in request.files:
            image = request.files['image']
            # Sube la imagen a Firebase Storage
            bucket = storage.bucket()
            blob = bucket.blob(image.filename)
            
            # Establece el tipo de contenido como 'image/png' (o el tipo de imagen adecuado)
            blob.upload_from_file(image, content_type='image/png')

            # Obtiene el nombre del archivo
            file_name = blob.name

            # Devuelve el nombre del archivo en la respuesta
            return jsonify({"fileName": file_name})
        else:
            return 'No se encontró ninguna imagen en la solicitud'
    @classmethod
    def create(cls):
        try:
            # Obtener los datos de la imagen del cuerpo de la solicitud JSON
            data = request.json
            url = data['url']
            descripcion = data['descripcion']

            new_img = Img(**data)
            print(new_img)
            # Llamar al método de clase 'create' del modelo de imagen para crear la imagen en la base de datos
            if Img.create(new_img):
                return jsonify({'message': 'Imagen creada exitosamente'}), 201
            else:
                return jsonify({'message': 'Error al crear imagen'}), 500
    
        except Exception as e:
            # Manejar cualquier error que ocurra durante el proceso de creación de la imagen
            return jsonify({'message': 'Error en la solicitud'}), 400

    @classmethod
    def get(cls, descripcion):
        try:
            imgs = Img.get(descripcion)  # Aquí se espera una lista de imágenes

            if imgs:
                serialized_imgs = [img.serialize() for img in imgs]
                return serialized_imgs, 200
            else:
                raise userNotFound(descripcion)  # Si no se encuentran imágenes, lanzar la excepción userNotFound
        except Exception as e:
            print("Error al obtener la imagen:", e)
            return jsonify({'message': 'Error en la solicitud'}), 500

    @classmethod
    def get_all(cls):
        """Get all imgs"""
        img_objects = Img.get_all()
        imgs = []
        for img in img_objects:
            imgs.append(img.serialize())
        return imgs, 200
    @classmethod
    def delete(cls, descripcion):
        try:
            # Eliminar todas las imágenes con el nombre del álbum (descripción) proporcionado
            if Img.delete(descripcion):
                return jsonify({'message': 'Imagen eliminada exitosamente'}), 200
            else:
                raise userNotFound(descripcion)  # Si no se encuentran imágenes para eliminar, lanzar la excepción userNotFound
        except Exception as e:
            print("Error al eliminar la imagen:", e)
            return jsonify({'message': 'Error en la solicitud'}), 500        