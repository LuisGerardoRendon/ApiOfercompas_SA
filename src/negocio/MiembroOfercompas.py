import json

from src.datos.EasyConnection import EasyConnection
from src.negocio import CodigosRespuesta, EstadoMiembro, TipoMiembro


class MiembroOfercompas():
    def __init__(self):
        self.idMiembro = None
        self.nickname = None
        self.email = None
        self.contrasenia = None
        self.estado = EstadoMiembro.ACTIVO
        self.tipoMiembro = TipoMiembro.COMUN

    def hacer_json(self):
        return json.dumps({"idMiembro": self.idMiembro,
                           "nickname": self.nickname,
                           "email": self.email,
                           "contrasenia": self.contrasenia,
                           "estado": self.estado,
                           "tipoMiembro": self.tipoMiembro
                           })

    def instanciar_con_hashmap(self, hash_miembro: dict):
        self.nickname = hash_miembro["nickname"]
        self.email = hash_miembro["email"]
        self.contrasenia = hash_miembro["contrasenia"]

    def hacer_json_token(self, token: str):
        return json.dumps({"idMiembro": int(self.idMiembro),
                           "nickname": self.nickname,
                           "email": self.email,
                           "contrasenia": self.contrasenia,
                           "estado": self.estado,
                           "tipoMiembro": self.tipoMiembro,
                           "token": token
                           })

    def convertir_a_json_efra(self) -> dict:
        diccionario = {}
        atributos = ["idMiembro", "nickname", "email", "contrasenia"]
        for key in atributos:
            if key in self.__dict__.keys():
                diccionario[key] = self.__getattribute__(key)
        return diccionario

    def convertir_a_json(self, atributos: list) -> dict:
        diccionario = {}
        diccionario["idMiembro"] = int(self.idMiembro)
        diccionario["tipoMiembro"] = int(self.tipoMiembro)
        diccionario["nickname"] = self.nickname
        diccionario["email"] = self.email
        diccionario["contrasenia"] = self.contrasenia
        diccionario["estado"] = int(self.estado)

        return diccionario

    def email_registrado(self) -> bool:
        status = False
        conexion = EasyConnection()
        query = "SELECT * FROM MiembroOfercompas WHERE email = %s;"
        values = [self.email]
        resultado = conexion.select(query, values)
        if len(resultado) > 0:
            status = True
        return status

    def nickname_registrado(self) -> bool:
        status = False
        conexion = EasyConnection()
        query = "SELECT * FROM MiembroOfercompas WHERE nickname = %s;"
        values = [self.nickname]
        resultado = conexion.select(query, values)
        if len(resultado) > 0:
            status = True
        return status

    def registrar(self) -> int:
        registrado = CodigosRespuesta.ERROR_INTERNO
        if not self.email_registrado() and not self.nickname_registrado():
            query = "INSERT INTO MiembroOfercompas(email, contrasenia, estado, tipoMiembro, nickname) VALUES " \
                    "(%s, %s, %s, %s, %s) ;"
            values = [self.email, self.contrasenia, self.estado, self.tipoMiembro, self.nickname]
            conexion = EasyConnection()
            conexion.send_query(query, values)
            self.idMiembro = self.getId()
            registrado = CodigosRespuesta.RECURSO_CREADO
        else:
            registrado = CodigosRespuesta.CONFLICTO
        return registrado

    def actualizar(self, old_email: str):
        actualizado = CodigosRespuesta.ERROR_INTERNO
        if not self.email_registrado_actualizar():
            query = "UPDATE MiembroOfercompas SET nickname = %s, email = %s, contrasenia = %s WHERE email = %s"
            values = [self.nickname, self.email, self.contrasenia, old_email]
            conexion = EasyConnection()
            conexion.send_query(query, values)
            actualizado = CodigosRespuesta.OK
        else:
            actualizado = CodigosRespuesta.CONFLICTO
        return actualizado

    def getId(self) -> int:
        id_recuperado = -1
        query = "SELECT idMiembro FROM MiembroOfercompas WHERE email = %s;"
        values = [self.email]
        conexion = EasyConnection()
        resultados = conexion.select(query, values)
        id_recuperado = resultados[0]["idMiembro"]
        return id_recuperado

    def email_registrado_actualizar(self) -> bool:
        status = False
        conexion = EasyConnection()
        self.idMiembro = self.getId()
        query = "SELECT * FROM MiembroOfercompas WHERE email = %s AND idMiembro <> %s;"
        values = [self.email, self.idMiembro]
        resultado = conexion.select(query, values)
        if len(resultado) > 0:
            status = True
        return status

    def expulsar(self) -> int:
        status = CodigosRespuesta.ERROR_INTERNO
        conexion = EasyConnection()
        query = "UPDATE MiembroOfercompas SET estado = 2 WHERE idMiembro = %s;"
        values = [self.idMiembro]
        resultado = conexion.send_query(query, values)
        status = CodigosRespuesta.OK
        return status

    def iniciar_sesion(self) -> int:
        status = CodigosRespuesta.ERROR_INTERNO
        conexion = EasyConnection()
        query = "SELECT * FROM MiembroOfercompas WHERE email = %s and contrasenia = %s and estado = 1;"
        values = [self.email, self.contrasenia]
        resultado = conexion.select(query, values)

        if len(resultado) > 0:
            self.idMiembro = int(resultado[0]["idMiembro"])
            self.tipoMiembro = resultado[0]["tipoMiembro"]
            self.nickname = resultado[0]["nickname"]
            status = CodigosRespuesta.OK
        else:
            status = CodigosRespuesta.NO_ENCONTRADO
        return status

    @staticmethod
    def obtener_miembros_mas_denunciados():
        query = "SELECT nickname, idMiembro, denuncias FROM MiembroOfercompas INNER JOIN" \
                " (SELECT publicador, COUNT(idPublicacion) AS denuncias FROM Publicacion WHERE" \
                " numeroDenuncias > 0 GROUP BY publicador ORDER BY COUNT(idPublicacion) DESC LIMIT 10)" \
                " AS DENUNCIAS ON idMiembro = DENUNCIAS.publicador;"
        conexion = EasyConnection()
        resultado = conexion.select(query)
        return resultado

    @staticmethod
    def obtener_reporte(id_miembro: int) -> dict:
        queryTolalPublicaciones = "SELECT COUNT(publicador) AS numeroPublicaciones FROM  Publicacion WHERE" \
                                  " publicador = %s;"
        queryTotalDenuncias = "SELECT SUM(numeroDenuncias) AS numeroDenuncias FROM  Publicacion WHERE publicador = %s;"
        queryTotalPuntuacion = "SELECT SUM(puntuacion) AS PuntuacionTotal FROM Publicacion WHERE publicador = %s;"
        queryTotalPublicacionesPositivas = "SELECT count(publicador) AS publicacionesPositivas FROM Publicacion " \
                                           "WHERE publicador = %s AND puntuacion >= 0;"

        values = [id_miembro]
        totalPublicaciones = 0
        totalDenuncias = 0
        totalPuntuacion = 0
        totalPublicacionesPositivas = 0;
        conexion = EasyConnection()
        resultado = conexion.select(queryTolalPublicaciones, values)
        if resultado:
            if resultado[0]["numeroPublicaciones"]:
                totalPublicaciones = int(resultado[0]["numeroPublicaciones"])

        resultado = conexion.select(queryTotalPuntuacion, values)

        if resultado:
            if resultado[0]["PuntuacionTotal"]:
                totalPuntuacion = int(resultado[0]["PuntuacionTotal"])

        resultado = conexion.select(queryTotalDenuncias, values)

        if resultado:
            if resultado[0]["numeroDenuncias"]:
                totalDenuncias = int(resultado[0]["numeroDenuncias"])

        resultado

        resultado = conexion.select(queryTotalPublicacionesPositivas, values)
        if resultado:
            if resultado[0]["publicacionesPositivas"]:
                totalPublicacionesPositivas = int(resultado[0]["publicacionesPositivas"])

        respuesta = {"numeroTotalPublicaciones": totalPublicaciones,
                     "puntuacionTotal": totalPuntuacion,
                     "numeroDenuncias": totalDenuncias,
                     "publicacionesPositivas": totalPublicacionesPositivas
                     }
        return respuesta




