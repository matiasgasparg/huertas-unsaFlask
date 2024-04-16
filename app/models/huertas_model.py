from ..database import DatabaseConnection
from app.models.date_model import Huertas_date
from ..models.exceptions import userNotFound,CustomException,InvalidDataError,duplicateError

class Huerta(Huertas_date):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    @classmethod
    def get(cls, idhuertas):
        """Obtener un usuario por su ID"""
        try:
            query = """SELECT idhuertas, titulo, direccion, descripcion,url
                       FROM huertas WHERE idhuertas = %s"""
            params = (idhuertas,)
            result = DatabaseConnection.fetch_one(query, params=params)

            if result is not None:
                return cls(**dict(zip(['idhuertas', 'titulo', 'direccion', 'descripcion','url'], result)))
            return None
        except Exception as e:
            print("Error al obtener las huertas:", e)
            return None
        finally:
            DatabaseConnection.close_connection()  # Cerrar la conexión después de realizar la consulta

    @classmethod
    def get_all(cls):
        """Obtener todos las huertas"""
        try:
            query = """SELECT idhuertas, titulo, direccion, descripcion,url 
                       FROM huertas"""
            results = DatabaseConnection.fetch_all(query)

            huertas = []
            if results:
                for result in results:
                    huertas.append(cls(**dict(zip(['idhuertas', 'titulo', 'direccion', 'descripcion','url'], result))))
            return huertas
        except Exception as e:
            print("Error al obtener todos los usuarios:", e)
            return None
        finally:
            DatabaseConnection.close_connection()  # Cerrar la conexión después de realizar la consulta
    @classmethod
    def create(cls, huerta):
        try:
            # Insertar la huerta en la base de datos
            query = """
                INSERT INTO huertas (titulo, direccion, descripcion,url) 
                VALUES (%s, %s, %s,%s)
            """
            params = (huerta.titulo, huerta.direccion, huerta.descripcion,huerta.url)
            DatabaseConnection.execute_query(query, params=params)

            return True
        except Exception as e:
            print("Error al crear la huerta:", e)
            return False
        finally:
            DatabaseConnection.close_connection()  # Cerrar la conexión después de realizar la consulta


    @classmethod
    def delete(cls, idhuertas):
        try:
            query_delete_relational = "DELETE FROM huertas_has_imagen WHERE huertas_idhuertas = %s"
            params = (idhuertas,)
            DatabaseConnection.execute_query(query_delete_relational, params=params)

            query_delete_huerta = "DELETE FROM huertas WHERE idhuertas = %s"
            DatabaseConnection.execute_query(query_delete_huerta, params=params)

            return {'message': 'Huerta eliminada exitosamente'}, 204
        except Exception as e:
            print("Error al eliminar la huerta:", e)
            return {'message': 'Error en la solicitud'}, 500
        finally:
            DatabaseConnection.close_connection()

    @classmethod
    def update(cls, idhuertas, data):
        try:
            for field, value in data.items():
                # Verificar si el campo es 'url' para actualizarlo de manera diferente
                if field == 'url':
                    query = "UPDATE huertas SET url = %s WHERE idhuertas = %s"
                    params = (value, idhuertas)
                    DatabaseConnection.execute_query(query, params=params)
                else:
                    # Actualizar otros campos de la misma manera que antes
                    query = f"UPDATE huertas SET {field} = %s WHERE idhuertas = %s"
                    params = (value, idhuertas)
                    DatabaseConnection.execute_query(query, params=params)

            return 'Datos actualizados exitosamente'
        except Exception as e:
            print("Error al actualizar los datos:", e)
            return 'Error en la solicitud'
        finally:
            DatabaseConnection.close_connection()  # Cierra la conexión después de realizar la consulta


    @classmethod
    def exists(cls, idhuertas):
        query = "SELECT COUNT(*) FROM huertas WHERE idhuertas = %s"
        params = (idhuertas,)
        result = DatabaseConnection.fetch_one(query, params=params)
        return result[0] > 0
