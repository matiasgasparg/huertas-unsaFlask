from ..database import DatabaseConnection
from app.models.date_model import Img_date
from ..models.exceptions import userNotFound,CustomException,InvalidDataError,duplicateError

class Img(Img_date):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    @classmethod
    def get_by_huerta(cls, idhuertas):
        try:
            # Consultar las imágenes relacionadas con la huerta
            query = """
                SELECT imagen.idimagen, imagen.url
                FROM imagen
                JOIN huertas_has_imagen ON imagen.idimagen = huertas_has_imagen.imagen_idimagen
                WHERE huertas_has_imagen.huertas_idhuertas = %s
            """
            params = (idhuertas,)
            results = DatabaseConnection.fetch_all(query, params=params)
    
            if results:
                # Si se encontraron resultados, devolver una lista de instancias de Img
                return [cls(**dict(zip(['idimagen', 'url'], row))) for row in results]
            else:
                return None
        except Exception as e:
            print("Error al obtener las imágenes:", e)
            return None
        finally:
            DatabaseConnection.close_connection()  # Cierra la conexión después de realizar la consulta
    @classmethod
    def get_all(cls):

        query = """SELECT idimagen, genero, url, descripcion,
        precio 
        FROM producto"""
        results = DatabaseConnection.fetch_all(query)

        imgs = []
        if results is not None:
            for result in results:
                imgs.append(cls(**dict(zip(['idimagen', 'genero', 'url', 'descripcion', 'precio'], result))))
            return imgs
    @classmethod
    def create(cls, url, idhuertas):
        try:
            # Insertar la imagen en la tabla imagen
            query = """INSERT INTO imagen (url) 
                       VALUES (%s)"""
            params = (url,)  # Corregido para que sea una tupla
            DatabaseConnection.execute_query(query, params=params)

            # Obtener el ID de la imagen recién insertada
            imagen_id = DatabaseConnection.fetch_one("SELECT LAST_INSERT_ID()")[0]

            # Insertar la relación en la tabla huertas_has_imagen
            query = """INSERT INTO huertas_has_imagen (huertas_idhuertas, imagen_idimagen) 
                       VALUES (%s, %s)"""
            params = (idhuertas, imagen_id)
            DatabaseConnection.execute_query(query, params=params)
            DatabaseConnection.close_connection()  # Cierra la conexión después de realizar la consulta 

            return True
        except Exception as e:
            print("Error al crear la imagen:", e)
            return False
   
    @classmethod
    def delete(cls, idimagen):
        try:
            # Eliminar la relación en la tabla huertas_has_imagen
            if cls.deleteRelationByImageId(idimagen):
                # Ahora que no hay dependencias en la tabla huertas_has_imagen, eliminar la imagen de la tabla imagen
                query = "DELETE FROM imagen WHERE idimagen = %s"
                params = (idimagen,)
                DatabaseConnection.execute_query(query, params=params)
                return True
            else:
                raise Exception("No se pudo eliminar la relación en la tabla huertas_has_imagen.")
        except Exception as e:
            print("Error al eliminar la imagen y su relación con la huerta:", e)
            return False
    @classmethod
    def deleteRelationByImageId(cls, idimagen):
        try:
            query = "DELETE FROM huertas_has_imagen WHERE imagen_idimagen = %s"
            params = (idimagen,)
            DatabaseConnection.execute_query(query, params=params)
            return True
        except Exception as e:
            print("Error al eliminar la relación en la tabla huertas_has_imagen:", e)
            return False


 