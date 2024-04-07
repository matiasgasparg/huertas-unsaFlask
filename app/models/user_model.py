from ..database import DatabaseConnection
from app.models.date_model import User_date
class User(User_date):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    @classmethod
    def get(cls, id_usuario):
        """Obtener un usuario por su ID"""
        try:
            query = """SELECT id_usuario, name, lastname, email,telefono
                       FROM usuarios WHERE id_usuario = %s"""
            params = (id_usuario,)
            result = DatabaseConnection.fetch_one(query, params=params)

            if result is not None:
                return cls(**dict(zip(['id_usuario', 'name', 'lastname', 'email','telefono'], result)))
            return None
        except Exception as e:
            print("Error al obtener usuario:", e)
            return None
        finally:
            DatabaseConnection.close_connection()  # Cerrar la conexión después de realizar la consulta

    @classmethod
    def get_all(cls):
        """Obtener todos los usuarios"""
        try:
            query = """SELECT id_usuario, name, lastname, email 
                       FROM usuarios"""
            results = DatabaseConnection.fetch_all(query)

            users = []
            if results:
                for result in results:
                    users.append(cls(**dict(zip(['id_usuario', 'name', 'username', 'email','telefono'], result))))
            return users
        except Exception as e:
            print("Error al obtener todos los usuarios:", e)
            return None
        finally:
            DatabaseConnection.close_connection()  # Cerrar la conexión después de realizar la consulta

    @classmethod
    def create(cls, user):
        """Crear un nuevo usuario"""
        try:
            query = """INSERT INTO usuarios (name, lastname, email,telefono) 
                       VALUES (%s, %s, %s, %s)"""
            params = (user.name, user.lastname, user.email,user.telefono)
            DatabaseConnection.execute_query(query, params=params)
            return True
        except Exception as e:
            print("Error al crear usuario:", e)
            return False
        finally:
            DatabaseConnection.close_connection()  # Cerrar la conexión después de realizar la consulta

    @classmethod
    def update(cls, id_usuario, campo, nuevo_valor):
        """Actualizar un usuario"""
        try:
            if campo == 'name':
                query = "UPDATE usuarios SET name = %s WHERE id_usuario = %s"
            elif campo == 'lastname':
                query = "UPDATE usuarios SET lastname = %s WHERE id_usuario = %s"
            elif campo == 'email':
                query = "UPDATE usuarios SET email = %s WHERE id_usuario = %s"
            else:
                raise ValueError("Campo no válido para actualización")
            params = (nuevo_valor, id_usuario)
            DatabaseConnection.execute_query(query, params=params)
            return True
        except Exception as e:
            print(f"Error al actualizar el campo '{campo}':", e)
            return False
        finally:
            DatabaseConnection.close_connection()  # Cerrar la conexión después de realizar la consulta

    @classmethod
    def delete(cls, id_usuario):
        """Eliminar un usuario"""
        try:
            query = "DELETE FROM usuarios WHERE id_usuario = %s"
            params = (id_usuario,)
            DatabaseConnection.execute_query(query, params=params)
            return True
        except Exception as e:
            print("Error al eliminar usuario:", e)
            return False
        finally:
            DatabaseConnection.close_connection()  # Cerrar la conexión después de realizar la consulta

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