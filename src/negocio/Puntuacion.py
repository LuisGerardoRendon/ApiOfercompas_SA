from http import HTTPStatus

from src.datos.EasyConnection import EasyConnection


class Puntuacion():
    def __init__(self):
        self.id_publicacion = None
        self.id_puntuador = None
        self.es_positiva = False

    def instanciar_con_hashmap(self, hash_puntuacion: dict, id_publicacion: int):
        self.id_publicacion = id_publicacion
        self.id_puntuador = hash_puntuacion["idMiembro"]
        self.es_positiva = hash_puntuacion["esPositiva"]

    def convertir_a_json(self) -> dict:
        diccionario = {}
        atributos = ["idPublicacion", "idPuntuador", "esPositiva"]
        for key in atributos:
            if key in self.__dict__.keys():
                diccionario[key] = self.__getattribute__(key)
        return diccionario

    def puntuar_publicacion(self) -> int:
        respuesta = HTTPStatus.CONFLICT
        if not Puntuacion.ha_puntuado(self.id_puntuador, self.id_publicacion):
            conexion = EasyConnection()
            query = "INSERT INTO Puntuacion (idPuntuador, idPublicacion, esPositiva) VALUES (%s, %s, %s)"
            values = [self.id_puntuador, self.id_publicacion, self.es_positiva]
            if conexion.send_query(query, values):

                query=""
                if self.es_positiva:
                    query = "UPDATE Publicacion SET puntuacion = puntuacion+1 WHERE idPublicacion = %s"
                else:
                    query = "UPDATE Publicacion SET puntuacion = puntuacion-1 WHERE idPublicacion = %s"

                values=[self.id_publicacion]
                if conexion.send_query(query, values):
                    respuesta = HTTPStatus.CREATED
                else:
                    respuesta = HTTPStatus.CONFLICT
            else:
                respuesta = HTTPStatus.INTERNAL_SERVER_ERROR
        return respuesta

    @staticmethod
    def ha_puntuado(id_miembro: int, id_publicacion: int) -> bool:
        conexion = EasyConnection()
        query = "SELECT idPuntuador FROM Puntuacion WHERE idPuntuador = %s AND idPublicacion = %s"
        values = [id_miembro, id_publicacion]
        resultado = conexion.select(query, values)
        return len(resultado) > 0

    @staticmethod
    def calcular_puntuacion(id_publicacion: int) -> int:
        conexion = EasyConnection()
        query = "SELECT COUNT(*) AS conteo FROM Puntuacion WHERE idPublicacion = %s AND esPositiva = 1"
        values = [id_publicacion]
        positivas = conexion.select(query, values)
        query = "SELECT COUNT(*) AS conteo FROM Puntuacion WHERE idPublicacion = %s AND esPositiva = 0"
        negativas = conexion.select(query, values)
        total = positivas[0]["conteo"] - negativas[0]["conteo"]
        return total
