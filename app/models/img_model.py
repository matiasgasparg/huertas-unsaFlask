from ..database import DatabaseConnection
from app.models.date_model import Img_date
from ..models.exceptions import userNotFound,CustomException,InvalidDataError,duplicateError

class Img(Img_date):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    @classmethod
    def get(cls, descripcion):
        try:
            descripcion = descripcion.upper()  # Convertir la descripción a mayúsculas

            query = """
                SELECT idimagen, url, descripcion
                FROM imagen WHERE descripcion = %s
            """
            params = (descripcion,)
            results = DatabaseConnection.fetch_all(query, params=params)
    
            if results:
                # Si se encontraron resultados, los convertimos en instancias de Img
                return [cls(**dict(zip(['idimagen', 'url', 'descripcion'], row))) for row in results]
            else:
                raise userNotFound(descripcion)  # Si no se encuentra la imagen, lanzar la excepción userNotFound
        except Exception as e:
            print("Error al obtener la imagen:", e)
            return None
        finally:
            DatabaseConnection.close_connection()  # Cerrar la conexión después de realizar la consulta
   

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
    def create(cls, img):
        try:
            query = """INSERT INTO imagen ( url, descripcion) 
                       VALUES (%s, %s)"""  # Corregir la consulta SQL
    
            params = (img.url, img.descripcion)  # Corregir la tupla de parámetros
            DatabaseConnection.execute_query(query, params=params)
            return True
        except Exception as e:
            print("Error al crear la IMAGEN:", e)
            return False
    @classmethod
    def delete(cls, descripcion):
        try:
            descripcion = descripcion.upper()
            query = """DELETE FROM imagen WHERE UPPER(descripcion) = %s"""
            params = (descripcion,)
            DatabaseConnection.execute_query(query, params=params)
            return True
        except Exception as e:
            print("Error al eliminar imágenes:", e)
            return False

 