from ..database import DatabaseConnection
from app.models.date_model import Not_date
from flask import Flask, request, jsonify

class Not(Not_date):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def get(cls, idnoticias):
        try:
            query = """
                SELECT p.idnoticias, p.titulo, p.subtitulo, p.contenido, p.fecha, GROUP_CONCAT(pi.url) AS urls
                FROM noticias p
                LEFT JOIN imagen_has_noticias phi ON p.idnoticias = phi.noticias_idnoticias
                LEFT JOIN imagen pi ON phi.imagen_idimagen = pi.idimagen
                WHERE p.idnoticias = %s
                GROUP BY p.idnoticias
            """
            result = DatabaseConnection.fetch_one(query, params=(idnoticias,))

            if result:
                idnoticias, titulo, subtitulo, contenido,fecha,urls = result
                noticia = cls(idnoticias=idnoticias, titulo=titulo,subtitulo=subtitulo, contenido=contenido, fecha=fecha)
                noticia.urls_imagenes = urls.split(',')
                return noticia
            else:
                return None
        except Exception as e:
            print("Error al obtener las noticias:", e)
            return None
        finally:
            DatabaseConnection.close_connection()  # Cerrar la conexión después de realizar la consulta
    @classmethod
    def get_all(cls):
        try:
           query = """
               SELECT p.idnoticias, p.titulo, p.subtitulo, p.contenido, p.fecha, GROUP_CONCAT(pi.url) AS urls
               FROM noticias p
               LEFT JOIN imagen_has_noticias phi ON p.idnoticias = phi.noticias_idnoticias
               LEFT JOIN imagen pi ON phi.imagen_idimagen = pi.idimagen
               GROUP BY p.idnoticias
           """
           results = DatabaseConnection.fetch_all(query)
    
           noticias = []
           for result in results:
                idnoticias, titulo, subtitulo, contenido,fecha, urls = result
    
                # Manejar el caso donde urls es None
                if urls is not None:
                    urls_list = urls.split(',')
                else:
                    urls_list = []
    
                noticia = Not(idnoticias=idnoticias, titulo=titulo,subtitulo=subtitulo, contenido=contenido, fecha=fecha,url=urls_list)
                noticias.append(noticia)
    
           return noticias
        except Exception as e:
           print("Error al obtener todos las noticias:", e)
           return None
        finally:
            DatabaseConnection.close_connection()  # Cerrar la conexión después de realizar la consulta

    @classmethod
    def create(cls, noti):
        try:
            # Insertar la noticia en la base de datos
            query = """
                INSERT INTO noticias (titulo, subtitulo, contenido, fecha) 
                VALUES (%s, %s, %s,%s)
            """
            params = (noti.titulo, noti.subtitulo, noti.contenido,noti.fecha)
            DatabaseConnection.execute_query(query, params=params)

            # Obtener el ID del noticias recién insertado
            query_get_last_insert_id = "SELECT LAST_INSERT_ID()"
            result = DatabaseConnection.fetch_one(query_get_last_insert_id)
            idnoticias = result[0]

            # Insertar las URLs asociadas a las imágenes en la tabla de imágenes
            for url in noti.url:
                query_insert_url = """
                    INSERT INTO imagen (url, descripcion) 
                    VALUES (%s, %s)
                """
                params_url = (url, noti.titulo)  # Asociar la misma descripción a todas las imágenes
                DatabaseConnection.execute_query(query_insert_url, params=params_url)

                # Obtener el ID de la imagen recién insertada
                query_get_last_insert_id = "SELECT LAST_INSERT_ID()"
                result = DatabaseConnection.fetch_one(query_get_last_insert_id)
                idimagen = result[0]

                # Establecer la relación entre el producto y la imagen en la tabla de relación
                query_insert_relation = """
                    INSERT INTO imagen_has_noticias (noticias_idnoticias, imagen_idimagen) 
                    VALUES (%s, %s)
                """
                params_relation = (idnoticias, idimagen)
                DatabaseConnection.execute_query(query_insert_relation, params=params_relation)

            return True
        except Exception as e:
            print("Error al crear las noticias:", e)
            return False
        finally:
            DatabaseConnection.close_connection()  # Cerrar la conexión después de realizar la consulta
    @classmethod
    def delete(cls, idnoticias):
        try:
            # Eliminar registros asociados en la tabla producto_has_imagen
            query_delete_relational = "DELETE FROM imagen_has_noticias WHERE noticias_idnoticias = %s"
            params = (idnoticias,)
            DatabaseConnection.execute_query(query_delete_relational, params=params)

            # Luego eliminar el producto
            query_delete_producto = "DELETE FROM noticias WHERE idnoticias = %s"
            DatabaseConnection.execute_query(query_delete_producto, params=params)

            return {'message': 'Noticia eliminada exitosamente'}, 204
        except Exception as e:
            print("Error al eliminar la noticia:", e)
            return {'message': 'Error en la solicitud'}, 500
        finally:
            DatabaseConnection.close_connection()  # Cerrar la conexión después de realizar la consulta
    @classmethod
    def update(cls, idnoticias, data):
        try:
            for field, value in data.items():
                if field == 'url':
                    cls.update_url(idnoticias, value)

                    # Aquí maneja la actualización de la URL
                    pass
                else:
                    # Aquí maneja la actualización de otros campos
                    query = f"UPDATE noticias SET {field} = %s WHERE idnoticias = %s"
                    params = (value, idnoticias)
                    DatabaseConnection.execute_query(query, params=params)
    
            return 'Datos actualizados exitosamente'
        except Exception as e:
            print("Error al actualizar los datos:", e)
            return 'Error en la solicitud'
        finally:
            DatabaseConnection.close_connection()  # Cierra la conexión después de realizar la consulta
    @classmethod
    def update_url(cls, idnoticias, urls):
        try:
            # Eliminar las entradas asociadas al noticia en la tabla de relación
            delete_query = "DELETE FROM imagen_has_noticias WHERE noticias_idnoticias = %s"
            DatabaseConnection.execute_query(delete_query, params=(idnoticias,))

            # Insertar las nuevas entradas en la tabla de relación
            for url in urls:
                # Insertar el URL en la tabla de imágenes
                insert_query = "INSERT INTO imagen (url) VALUES (%s)"  # Query original
                # Ajustar la URL para que se almacene correctamente en la base de datos
                adjusted_url = url.get('url')  # Obtener el valor de la URL del JSON enviado por el front
                DatabaseConnection.execute_query(insert_query, params=(adjusted_url,))
                # Obtener el ID de la imagen recién insertada
                imagen_id = DatabaseConnection.fetch_one("SELECT LAST_INSERT_ID()")[0]
                # Establecer la relación entre el noticia y la imagen en la tabla de relación
                insert_relation_query = "INSERT INTO imagen_has_noticias (noticias_idnoticias, imagen_idimagen) VALUES (%s, %s)"
                DatabaseConnection.execute_query(insert_relation_query, params=(idnoticias, imagen_id))

            return 'URLs actualizados exitosamente'
        except Exception as e:
            print("Error al actualizar la URL:", e)
            return 'Error en la solicitud'
        finally:
            DatabaseConnection.close_connection()  # Cierra la conexión después de realizar la consulta

    
    @classmethod
    def exists(cls, idnoticias):
        query = "SELECT COUNT(*) FROM noticias WHERE idnoticias = %s"
        params = (idnoticias,)
        result = DatabaseConnection.fetch_one(query, params=params)
        return result[0] > 0