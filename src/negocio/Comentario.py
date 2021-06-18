import json
from http import HTTPStatus
from src.datos.EasyConnection import EasyConnection


class Comentario():
    def __init__(self):
        self.id_miembro = None
        self.id_publicacion = None
        self.contenido = None
        self.nickname = None

    def hacer_json_sin_nickname(self):
        return json.dumps({"idPublicacion": self.id_publicacion,
                           "idMiembro": self.id_miembro,
                           "contenido": self.contenido
                           })

    def hacer_json_nickname_contenido(self) -> dict:
        diccionario ={"nickname" : self.nickname,
                      "contenido": self.contenido
                      }
        return diccionario




    def instanciar_con_hashmap(self, hash_comentario: dict, id_publicacion):
        self.id_miembro = hash_comentario["idMiembro"]
        self.id_publicacion = id_publicacion
        self.contenido = hash_comentario["contenido"]

    def registrar(self) -> int:
        status = HTTPStatus.INTERNAL_SERVER_ERROR
        if self.existe_publicacion() and self.existe_miembro():
            conexion = EasyConnection()
            query = "INSERT INTO Comentario(idMiembro, idPublicacion, contenido) VALUES" \
                    "(%s, %s, %s)"
            values = [self.id_miembro, self.id_publicacion, self.contenido]
            conexion.send_query(query, values)
            status = HTTPStatus.CREATED
        else:
            status = HTTPStatus.NOT_FOUND
        return status

    def existe_publicacion(self) -> bool:
        existe = False
        query = "SELECT * FROM Publicacion WHERE idPublicacion = %s AND estado = 1;"
        values = [self.id_publicacion]
        conexion = EasyConnection()
        resultado = conexion.select(query, values)
        if len(resultado) > 0:
            existe = True

        return existe

    def existe_miembro(self) -> bool:
        existe = False
        query = "SELECT * FROM MiembroOfercompas WHERE idMiembro = %s;"
        values = [self.id_miembro]
        conexion = EasyConnection()
        resultado = conexion.select(query, values)
        if len(resultado) > 0:
            existe = True

        return existe

    @staticmethod
    def obtener_comentarios(idPublicacion: int):
        conexion = EasyConnection()
        query = "SELECT Comentario.contenido,MiembroOfercompas.nickname FROM Comentario INNER JOIN " \
                "MiembroOfercompas ON Comentario.idMiembro=MiembroOfercompas.idMiembro " \
                "WHERE idPublicacion = %s;"
        values = [idPublicacion]
        comentarios_obtenidos = conexion.select(query, values)
        resultado = []
        if comentarios_obtenidos:
            for comentario_invididual in comentarios_obtenidos:
                comentario_aux = Comentario()
                comentario_aux.contenido = comentario_invididual["contenido"]
                comentario_aux.nickname = comentario_invididual["nickname"]
                resultado.append(comentario_aux)
        print(resultado)
        return resultado
