from ..database import DatabaseConnection
from app.models.date_model import User_date
class User(User_date):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    @classmethod
    def get_asistencia(cls, idhuertas, id_practica):
        """Obtener la asistencia de todos los usuarios para una práctica específica y una huerta determinada"""
        try:
            query = """
                SELECT usuarios.id_usuario, usuarios.name, usuarios.lastname, usuarios.email, usuarios.telefono, asistencia.asistio
                FROM usuarios
                INNER JOIN asistencia ON usuarios.id_usuario = asistencia.id_usuario
                INNER JOIN practica_asistencia ON asistencia.id_asistencia = practica_asistencia.id_asistencia
                INNER JOIN huertas_has_usuarios ON usuarios.id_usuario = huertas_has_usuarios.usuarios_id_usuario
                WHERE huertas_has_usuarios.huertas_idhuertas = %s AND practica_asistencia.idpractica = %s
            """
            params = (idhuertas, id_practica)
            results = DatabaseConnection.fetch_all(query, params=params)

            if results is not None:
                return [cls(**dict(zip(['id_usuario', 'name', 'lastname', 'email', 'telefono', 'asistio'], row))) for row in results]
            return None
        except Exception as e:
            print("Error al obtener la asistencia de los usuarios:", e)
            return None
        finally:
            DatabaseConnection.close_connection()  # Cerrar la conexión después de realizar la consulta

    @classmethod
    def get(cls, idhuertas):
        """Obtener un usuario por su ID"""
        try:
            query = """SELECT usuarios.id_usuario, usuarios.name, usuarios.lastname, usuarios.email, usuarios.telefono,usuarios.asistio
                       FROM usuarios
                       JOIN huertas_has_usuarios ON usuarios.id_usuario = huertas_has_usuarios.usuarios_id_usuario
                       WHERE huertas_has_usuarios.huertas_idhuertas = %s
                    """
            
            params = (idhuertas,)
            results = DatabaseConnection.fetch_all(query, params=params)

            if results is not None:
                return  [cls(**dict(zip(['id_usuario', 'name', 'lastname', 'email','telefono','asistio'], row))) for row in results]
            return None
        except Exception as e:
            print("Error al obtener usuario:", e)
            return None
        finally:
            DatabaseConnection.close_connection()  # Cerrar la conexión después de realizar la consulta


    @classmethod
    def create(cls, user,idhuertas):
        """Crear un nuevo usuario"""
        try:
            query = """INSERT INTO usuarios (name, lastname, email,telefono) 
                       VALUES (%s, %s, %s, %s)"""
            params = (user.name, user.lastname, user.email,user.telefono)
            DatabaseConnection.execute_query(query, params=params)
            
            # Obtener el ID del usuario recién insertado
            huertas_id = DatabaseConnection.fetch_one("SELECT LAST_INSERT_ID()")[0]

            # Insertar la relación en la tabla huertas_has_usuarios
            query = """INSERT INTO huertas_has_usuarios (huertas_idhuertas, usuarios_id_usuario) 
                       VALUES (%s, %s)"""
            params = (idhuertas, huertas_id)
            DatabaseConnection.execute_query(query, params=params)

            return True
        except Exception as e:
            print("Error al crear usuario:", e)
            return False
        finally:
            DatabaseConnection.close_connection()  # Cerrar la conexión después de realizar la consulta

    @staticmethod
    def registrar_asistencia(id_usuario, id_practica, asistio):
        try:
            # Registrar la asistencia en la tabla 'asistencia'
            query_asistencia = "INSERT INTO asistencia (id_usuario, asistio) VALUES (%s, %s)"
            params_asistencia = (id_usuario, asistio)
            DatabaseConnection.execute_query(query_asistencia, params=params_asistencia)

            # Obtener el ID de la asistencia recién insertada
            id_asistencia = DatabaseConnection.fetch_one("SELECT LAST_INSERT_ID()")[0]

            # Registrar la relación en la tabla 'practica_asistencia'
            query_practica_asistencia = "INSERT INTO practica_asistencia (idpractica, id_asistencia) VALUES (%s, %s)"
            params_practica_asistencia = (id_practica, id_asistencia)
            DatabaseConnection.execute_query(query_practica_asistencia, params=params_practica_asistencia)

            return True
        except Exception as e:
            print("Error al registrar la asistencia:", e)
            return False
        finally:
            DatabaseConnection.close_connection()

    @staticmethod
    def tiene_asistencia_registrada(id_usuario, id_practica):
        query = "SELECT COUNT(*) FROM asistencia " \
                "INNER JOIN practica_asistencia " \
                "ON asistencia.id_asistencia = practica_asistencia.id_asistencia " \
                "WHERE asistencia.id_usuario = %s AND practica_asistencia.idpractica = %s"
        params = (id_usuario, id_practica)
        result = DatabaseConnection.fetch_one(query, params=params)
        return result and result[0] > 0
    @classmethod
    def delete(cls,id_usuario):
        try:
            # Eliminar la relación en la tabla huertas_has_imagen
            if cls.deleteRelationByImageId(id_usuario):
                # Ahora que no hay dependencias en la tabla huertas_has_imagen, eliminar la imagen de la tabla imagen
                query = "DELETE FROM usuarios WHERE id_usuario = %s"
                params = (id_usuario,)
                DatabaseConnection.execute_query(query, params=params)
                return True
            else:
                raise Exception("No se pudo eliminar la relación en la tabla.")
        except Exception as e:
            print("Error al eliminar la imagen y su relación con la huerta:", e)
            return False
    @classmethod
    def deleteRelationByImageId(cls, id_usuario):
        try:
            query = "DELETE FROM huertas_has_usuarios WHERE usuarios_id_usuario = %s"
            params = (id_usuario,)
            DatabaseConnection.execute_query(query, params=params)
            return True
        except Exception as e:
            print("Error al eliminar la relación en la tabla:", e)
            return False


    @classmethod
    def exists(cls, id_usuario):
        """Verificar si un usuario existe"""
        try:
            query = "SELECT COUNT(*) FROM usuarios WHERE id_usuario = %s"
            params = (id_usuario,)
            result = DatabaseConnection.fetch_one(query, params=params)
            return result[0] > 0
        except Exception as e:
            print("Error al verificar la existencia del usuario:", e)
            return False
        finally:
            DatabaseConnection.close_connection()  # Cerrar la conexión después de realizar la consulta

    @classmethod
    def duplicate(cls, username, email):
        """Verificar si hay duplicados en el nombre de usuario o correo electrónico"""
        try:
            query = "SELECT COUNT(*) FROM usuarios WHERE username = %s OR email = %s"
            params = (username, email)
            result = DatabaseConnection.fetch_one(query, params=params)
            count = result[0]
            return count > 0
        except Exception as e:
            print("Error al verificar duplicados de usuario:", e)
            return False
        finally:
            DatabaseConnection.close_connection()  # Cerrar la conexión después de realizar la consulta

    @classmethod
    def logout(cls, id_usuario):
        """Cerrar sesión de un usuario"""
        try:
            query = "UPDATE usuarios SET is_logged_in = %s WHERE id_usuario = %s"
            params = (False, id_usuario)
            DatabaseConnection.execute_query(query, params=params)
            return True
        except Exception as e:
            print("Error al cerrar sesión del usuario:", e)
            return False
        finally:
            DatabaseConnection.close_connection()  # Cerrar la conexión después de realizar la consulta