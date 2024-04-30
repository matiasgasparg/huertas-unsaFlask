from ..database import DatabaseConnection

class Practica:
    def __init__(self, idpractica=None, descripcion=None, fecha=None, responsables=None):
        self.idpractica = idpractica
        self.descripcion = descripcion
        self.fecha = fecha
        self.responsables = responsables

    @classmethod
    def get(cls, idhuertas):
        try:
            query = """
                SELECT practica.idpractica, practica.descripcion, practica.fecha, practica.responsables
                FROM practica
                JOIN practica_huertas ON practica.idpractica = practica_huertas.idpractica
                WHERE practica_huertas.idhuertas = %s
            """
            params = (idhuertas,)
            results = DatabaseConnection.fetch_all(query, params=params)

            if results is not None:
                return [cls(*row) for row in results]
            return None
        except Exception as e:
            print("Error al obtener las prácticas:", e)
            return None
        finally:
            DatabaseConnection.close_connection()

    @classmethod
    def create(cls, practica, idhuertas):
        try:
            query = "INSERT INTO practica (descripcion, fecha, responsables,titulo) VALUES (%s, %s, %s,%s)"
            params = (practica.descripcion, practica.fecha, practica.responsables,practica.titulo)
            DatabaseConnection.execute_query(query, params=params)
            
            # Obtener el ID de la práctica recién insertada
            practica_id = DatabaseConnection.fetch_one("SELECT LAST_INSERT_ID()")[0]

            # Insertar la relación en la tabla huertas_has_practica
            query = "INSERT INTO practica_huertas (idhuertas, idpractica) VALUES (%s, %s)"
            params = (idhuertas, practica_id)
            DatabaseConnection.execute_query(query, params=params)

            return True
        except Exception as e:
            print("Error al crear la práctica:", e)
            return False
        finally:
            DatabaseConnection.close_connection()

    @classmethod
    def update(cls, idpractica, descripcion, fecha, responsables,titulo):
        try:
            query = """
                UPDATE practica
                SET descripcion = %s, fecha = %s, responsables = %s, titulo =%s
                WHERE idpractica = %s
            """
            params = (descripcion, fecha, responsables,titulo,idpractica)
            DatabaseConnection.execute_query(query, params=params)
            return True
        except Exception as e:
            print("Error al actualizar la práctica:", e)
            return False
        finally:
            DatabaseConnection.close_connection()

    @classmethod
    def delete(cls, idpractica):
        try:
            # Eliminar las filas relacionadas en la tabla practica_huertas primero
            query = "DELETE FROM practica_huertas WHERE idpractica = %s"
            params = (idpractica,)
            DatabaseConnection.execute_query(query, params=params)


            query= "DELETE FROM practica_asistencia WHERE idpractica= %s"
            DatabaseConnection.execute_query(query, params=params)
            
            # Luego eliminar la fila de la tabla practica
            query = "DELETE FROM practica WHERE idpractica = %s"
            DatabaseConnection.execute_query(query, params=params)


            return True
        except Exception as e:
            print("Error al eliminar la práctica:", e)
            return False
        finally:
            DatabaseConnection.close_connection()


    def serialize(self):
        return {
            'idpractica': self.idpractica,
            'descripcion': self.descripcion,
            'fecha': self.fecha,
            'responsables': self.responsables,
            'titulo': self.titulo
        }
