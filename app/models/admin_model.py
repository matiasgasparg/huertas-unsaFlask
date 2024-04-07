from ..database import DatabaseConnection
from app.models.date_model import Admin_date
class Admin(Admin_date):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    @classmethod
    def get_all(cls):
        """Obtener todos los usuarios"""
        try:
            query = """SELECT id_admin, email, password 
                       FROM admin"""
            results = DatabaseConnection.fetch_all(query)

            users = []
            if results:
                for result in results:
                    users.append(cls(**dict(zip(['id_admin', 'email', 'password'], result))))
            return users
        except Exception as e:
            print("Error al obtener todos los usuarios:", e)
            return None
        finally:
            DatabaseConnection.close_connection()  # Cerrar la conexión después de realizar la consulta
