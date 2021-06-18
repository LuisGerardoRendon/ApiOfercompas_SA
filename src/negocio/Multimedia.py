from http import HTTPStatus

from src.datos.EasyConnection import EasyConnection
from src.negocio.Publicacion import Publicacion
from src.transferencia_archivos.ServidorArchivos import ServidorArchivos


class Multimedia:
    def registrar_imagen(self, ruta: str, id_publicacion: int) -> int:
        resultado = HTTPStatus.INTERNAL_SERVER_ERROR
        conexion = EasyConnection()
        query = "INSERT INTO Multimedia(ruta, idOferta, tipo) VALUES (%s, %s, 'foto');"
        values = [ruta, id_publicacion]
        conexion.send_query(query, values)
        resultado = HTTPStatus.CREATED
        return resultado

    def registrar_video(self, ruta: str, id_publicacion: int) -> int:
        resultado = HTTPStatus.INTERNAL_SERVER_ERROR
        conexion = EasyConnection()
        query = "INSERT INTO Multimedia(ruta, idOferta, tipo) VALUES (%s, %s, 'video');"
        values = [ruta, id_publicacion]
        conexion.send_query(query, values)
        resultado = HTTPStatus.CREATED
        return resultado

    def obtener_ruta_foto_id(self, id_publicacion: int) -> str:
        conexion = EasyConnection()
        query = "SELECT ruta FROM Multimedia WHERE idOferta = %s AND tipo = 'foto'"
        values = [id_publicacion]
        ruta = conexion.select(query, values)
        ruta_retorno = "not"
        if len(ruta) > 0:
            ruta_retorno = ruta[0]["ruta"]
        return ruta_retorno

    def obtener_ruta_video_id(self, id_publicacion: int) -> str:
        conexion = EasyConnection()
        query = "SELECT ruta FROM Multimedia WHERE idOferta = %s AND tipo = 'video'"
        values = [id_publicacion]
        ruta = conexion.select(query, values)
        ruta_retorno = "not"
        if len(ruta) > 0:
            ruta_retorno = ruta[0]["ruta"]
        return ruta_retorno

    def recuperar_archivo(self, ruta_archivo):
        servidor = ServidorArchivos()
        resultado = servidor.obtener_archivos(ruta_archivo)
        imagen = resultado[0]
        return imagen

    def actualizar_imagen(self, ruta: str, id_publicacion: int) -> int:
        resultado = HTTPStatus.INTERNAL_SERVER_ERROR
        conexion = EasyConnection()
        query = "UPDATE Multimedia SET ruta = %s WHERE idOferta = %s AND tipo = 'foto'"
        values = [ruta, id_publicacion]
        conexion.send_query(query, values)
        resultado = HTTPStatus.CREATED
        return resultado

    def actualizar_video(self, ruta: str, id_publicacion: int) -> int:
        resultado = HTTPStatus.INTERNAL_SERVER_ERROR
        conexion = EasyConnection()
        query = "UPDATE Multimedia SET ruta = %s WHERE idOferta = %s AND tipo = 'video'"
        values = [ruta, id_publicacion]
        conexion.send_query(query, values)
        resultado = HTTPStatus.CREATED
        return resultado
