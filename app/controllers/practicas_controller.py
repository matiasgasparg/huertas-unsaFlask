from flask import jsonify, request
from ..models.practicas_model import Practica

class practicasController:
    @classmethod
    def get(cls, idhuertas):
        try:
            practicas = Practica.get(idhuertas)
            if practicas:
                serialized_practicas = [practica.serialize() for practica in practicas]
                return jsonify(serialized_practicas), 200
            else:
                return jsonify({'message': 'No se encontraron prácticas para la huerta'}), 404
        except Exception as e:
            print("Error al obtener las prácticas:", e)
            return jsonify({'message': 'Error en la solicitud'}), 500

    @classmethod
    def create(cls, idhuertas):
        try:
            data = request.json
            titulo= data['titulo']
            descripcion = data['descripcion']
            fecha = data['fecha']
            responsables = data['responsables']
            
            new_practica = Practica(titulo=titulo,descripcion=descripcion, fecha=fecha, responsables=responsables)

            if Practica.create(new_practica, idhuertas):
                return jsonify({'message': 'Práctica creada exitosamente'}), 201
            else:
                return jsonify({'message': 'Error al crear práctica'}), 500
        except Exception as e:
            return jsonify({'message': 'Error en la solicitud'}), 400

    @classmethod
    def update(cls, idpractica):
        try:
            data = request.json
            titulo = data.get('titulo')
            descripcion = data.get('descripcion')
            fecha = data.get('fecha')
            responsables = data.get('responsables')

            if not (titulo or descripcion or fecha or responsables):
                return jsonify({'message': 'No se proporcionaron datos para actualizar'}), 400

            if Practica.update(idpractica,titulo,descripcion, fecha, responsables):
                return jsonify({'message': 'Práctica actualizada exitosamente'}), 200
            else:
                return jsonify({'message': 'No se encontró la práctica'}), 404
        except Exception as e:
            print("Error al actualizar la práctica:", e)
            return jsonify({'message': 'Error en la solicitud'}), 500

    @classmethod
    def delete(cls, idpractica):
        try:
            if Practica.delete(idpractica):
                return jsonify({'message': 'Práctica eliminada exitosamente'}), 200
            else:
                return jsonify({'message': 'No se encontró la práctica'}), 404
        except Exception as e:
            print("Error al eliminar la práctica:", e)
            return jsonify({'message': 'Error en la solicitud'}), 500