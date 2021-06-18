from http import HTTPStatus

from src.datos.EasyConnection import EasyConnection
from src.negocio.Publicacion import Publicacion


class CodigoDescuento(Publicacion):

    def __init__(self):
        super().__init__()
        self.codigo = None
        self.tipoPublicacion = "CodigoDescuento"

    def convertir_a_json(self) -> dict:
        diccionario = {}
        atributos = ["idPublicacion", "titulo", "descripcion", "codigo", "fechaCreacion", "fechaFin", "publicador",
                     "categoria"]
        for key in atributos:
            if key in self.__dict__.keys():
                diccionario[key] = self.__getattribute__(key)
        return diccionario

    def registrar_codigo(self) -> int:
        respuesta = 500
        conexion = EasyConnection()
        query = "CALL SPI_registrarCodigoDescuento (%s, %s, %s, %s, %s, %s, %s)"
        values = [self.titulo, self.descripcion, self.fechaCreacion, self.fechaFin, self.categoria,
                  self.codigo, self.publicador]
        resultado = conexion.select(query, values)
        print("caca")
        print(resultado)

        if resultado:
            self.idPublicacion = resultado[0]["idPublicacion"]
            respuesta = HTTPStatus.CREATED
        else:
            respuesta = 400

        return respuesta

    def actualizar_codigo(self, id_publicacin: int) -> int:
        respuesta = HTTPStatus.INTERNAL_SERVER_ERROR
        conexion = EasyConnection()
        query = "CALL SPA_actualizarCodigoDescuento(%s, %s, %s, %s, %s, %s, %s)"
        values = [id_publicacin, self.titulo, self.descripcion, self.fechaCreacion,
                  self.fechaFin, self.categoria, self.codigo]
        if conexion.send_query(query, values):
            respuesta = HTTPStatus.OK
        else:
            respuesta = HTTPStatus.BAD_REQUEST

        return respuesta

    @staticmethod
    def obtener_codigo(pagina: int, categoria: int):
        conexion = EasyConnection()
        query = "CALL SPS_obtenerCodigosDescuento(%s, %s)"
        values = [pagina, categoria]
        codigos_obtenidos = conexion.select(query, values)
        resultado = []
        if codigos_obtenidos:
            for codigo_individual in codigos_obtenidos:
                codigo_aux = CodigoDescuento()
                codigo_aux.idPublicacion = codigo_individual["idPublicacion"]
                codigo_aux.titulo = codigo_individual["titulo"]
                codigo_aux.descripcion = codigo_individual["descripcion"]
                codigo_aux.fechaCreacion = str(codigo_individual["fechaCreacion"])
                codigo_aux.fechaFin = str(codigo_individual["fechaFin"])
                codigo_aux.codigo = codigo_individual["codigo"]
                codigo_aux.obtener_puntuacion()
                resultado.append(codigo_aux)
        return resultado
