class User_date:
    def __init__(self, **kwargs):
        self.id_usuario = kwargs.get('id_usuario')
        self.name = kwargs.get('name')
        self.lastname = kwargs.get('lastname')
        self.email = kwargs.get('email')
        self.telefono = kwargs.get('telefono')
        self.asistio= kwargs.get('asistio')

    def serialize(self):
        return {
            "id_usuario": self.id_usuario,
            "name": self.name,
            "lastname": self.lastname,
            "email": self.email,
            "telefono": self.telefono,
            "asistio":self.asistio


        }
class Img_date:
    def __init__(self, **kwargs):
        self.idimagen = kwargs.get('idimagen')
        self.url = kwargs.get('url')
        self.descripcion = kwargs.get('descripcion') 
        self.idhuertas= kwargs.get('idhuertas')


    def serialize(self):
        return {
            "idimagen": self.idimagen,
            "url": self.url,
            "descripcion": self.descripcion,
            "idhuertas":self.idhuertas
        }
       
class Not_date:
    def __init__(self, **kwargs):
        self.idnoticias = kwargs.get('idnoticias')
        self.titulo = kwargs.get('titulo')
        self.url = kwargs.get('url')
        self.subtitulo = kwargs.get('subtitulo')
        self.contenido = kwargs.get('contenido') 
        self.fecha = kwargs.get('fecha')



    def serialize(self):
        return {
            "idnoticias": self.idnoticias,
            "titulo": self.titulo,
            "url": self.url,
            "subtitulo": self.subtitulo,
            "contenido": self.contenido,
            "fecha": self.fecha
        }
class Admin_date:
    def __init__(self, **kwargs):
        self.id_admin = kwargs.get("id_admin")
        self.email = kwargs.get("email")
        self.password = kwargs.get("password")
        self.admin = kwargs.get('admin')  

    def serialize(self):
        return{
        'id_admin': self.id_admin,
        "email": self.email,
        "password": self.password,
        "admin": self.admin
    }

class Huertas_date:
    def __init__(self,**kwargs):
        self.idhuertas = kwargs.get("idhuertas")   
        self.titulo = kwargs.get("titulo")
        self.direccion= kwargs.get("direccion")
        self.descripcion = kwargs.get("descripcion")
        self.url = kwargs.get("url")
    def serialize (self):
        return{
            'idhuertas': self.idhuertas,
            'titulo': self.titulo,
            'direccion': self.direccion,
            'descripcion': self.descripcion,
            'url': self.url
        }


