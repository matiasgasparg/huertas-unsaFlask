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
    def create(cls, idhuertas):
        try:
            # Obtener los datos de la solicitud JSON
            data = request.json
            
            # Verificar si 'urls' está presente en los datos recibidos y si es una lista
            if 'urls' in data and isinstance(data['urls'], list):
                urls = data['urls']
        
                for url in urls:
                    # Llamar al método create de la clase Img para crear la imagen en la base de datos
                    if not Img.create(url, idhuertas):
                        # Si hay un error al crear la imagen, devolver un mensaje de error
                        return jsonify({'message': 'Error al crear imágenes'}), 500
        
                # Si todas las imágenes se crean correctamente, devolver un mensaje de éxito
                return jsonify({'message': 'Imágenes creadas exitosamente'}), 200
            else:
                return jsonify({'message': 'No se proporcionó una lista de URLs válida'}), 400
        
        except Exception as e:
            # Manejar cualquier error que ocurra durante el proceso de creación de las imágenes
            print("Error al crear las imágenes:", e)
            return jsonify({'message': 'Error en la solicitud'}), 400


    @classmethod
    def get_by_huerta(cls, idhuertas):
        try:
            # Llamar al método get_by_huerta de la clase Img para obtener las imágenes de la huerta
            imgs = Img.get_by_huerta(idhuertas)
            
            # Serializar las imágenes y devolverlas como respuesta
            if imgs:
                serialized_imgs = [img.serialize() for img in imgs]
                return jsonify(serialized_imgs), 200
            else:
                return jsonify({'message': 'No se encontraron imágenes para la huerta'}), 404
        except Exception as e:
            print("Error al obtener las imágenes:", e)
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
    def delete(cls, idimagen):
        try:
            # Eliminar la imagen de la tabla imagen
            if Img.delete(idimagen):
                # Eliminar la relación en la tabla huertas_has_imagen
                if Img.deleteRelationByImageId(idimagen):
                    return jsonify({'message': 'Imagen eliminada exitosamente'}), 200
                else:
                    raise userNotFound(f"La relación huertas_has_imagen no se encontró para idimagen {idimagen} e idhuerta {idhuerta}")
            else:
                raise userNotFound(f"La imagen no se encontró para idimagen {idimagen}")
        except Exception as e:
            print("Error al eliminar la imagen:", e)
            return jsonify({'message': 'Error en la solicitud'}), 500