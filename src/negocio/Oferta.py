from http import HTTPStatus

from src.datos.EasyConnection import EasyConnection
from src.negocio.Publicacion import Publicacion


class Oferta(Publicacion):

    def __init__(self):
        super().__init__()
        self.precio = None
        self.vinculo = None
        self.tipoPublicacion = "Oferta"

    def convertir_a_json(self) -> dict:
        diccionario = {}
        atributos = ["idPublicacion", "titulo", "descripcion", "fechaCreacion", "fechaFin", "precio", "vinculo",
                     "puntuacion", "publicador", "categoria"]
        for key in atributos:
            if key in self.__dict__.keys():
                diccionario[key] = self.__getattribute__(key)
        diccionario["imagen"] = "http://127.0.0.1:5000/publicaciones/" + str(self.idPublicacion) + "/imagenes"
        diccionario["video"] = "http://127.0.0.1:5000/publicaciones/" + str(self.idPublicacion) + "/videos"
        return diccionario

    def registrar_oferta(self) -> int:
        respuesta = HTTPStatus.INTERNAL_SERVER_ERROR
        conexion = EasyConnection()
        query = "CALL SPI_registrarOferta (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = [self.titulo, self.descripcion, self.precio, self.fechaCreacion, self.fechaFin, self.categoria,
                  self.vinculo, self.publicador]
        print(values)
        resultado = conexion.select(query, values)
        if resultado:
            self.idPublicacion = resultado[0]["idPublicacion"]
            respuesta = HTTPStatus.CREATED
        else:
            respuesta = HTTPStatus.BAD_REQUEST
        return respuesta

    def actualizar_oferta(self, id_publicacin: int) -> int:
        respuesta = HTTPStatus.INTERNAL_SERVER_ERROR
        conexion = EasyConnection()
        query = "CALL SPA_actualizarOferta(%s, %s, %s, %s, %s, %s, %s, %s)"
        values = [id_publicacin, self.titulo, self.descripcion, self.precio, self.fechaCreacion,
                  self.fechaFin, self.categoria, self.vinculo]
        if conexion.send_query(query, values):
            respuesta = HTTPStatus.OK
        else:
            respuesta = HTTPStatus.BAD_REQUEST

        return respuesta

    @staticmethod
    def obtener_oferta(pagina: int, categoria: int):
        conexion = EasyConnection()
        query = "CALL SPS_obtenerOfertasGeneral(%s, %s)"
        values = [pagina, categoria]
        ofertas_obtenidas = conexion.select(query, values)
        resultado = []
        if ofertas_obtenidas:
            for oferta_individual in ofertas_obtenidas:
                oferta_aux = Oferta()
                oferta_aux.idPublicacion = oferta_individual["idPublicacion"]
                oferta_aux.titulo = oferta_individual["titulo"]
                oferta_aux.descripcion = oferta_individual["descripcion"]
                oferta_aux.fechaCreacion = str(oferta_individual["fechaCreacion"])
                oferta_aux.fechaFin = str(oferta_individual["fechaFin"])
                oferta_aux.precio = oferta_individual["precio"]
                oferta_aux.vinculo = oferta_individual["vinculo"]
                oferta_aux.publicador = oferta_individual["publicador"]
                oferta_aux.puntuacion = oferta_individual["puntuacion"]
                resultado.append(oferta_aux)
        return resultado

    @staticmethod
    def obtener_por_id_publicador(pagina: int, id_publicador: int):
        conexion = EasyConnection()
        query = "CALL SPS_obtenerOfertasPorPublicador(%s, %s)"
        values = [pagina, id_publicador]
        ofertas_obtenidas = conexion.select(query, values)
        resultado = []
        if ofertas_obtenidas:
            for oferta_individual in ofertas_obtenidas:
                oferta_aux = Oferta()
                oferta_aux.idPublicacion = oferta_individual["idPublicacion"]
                oferta_aux.titulo = oferta_individual["titulo"]
                oferta_aux.descripcion = oferta_individual["descripcion"]
                oferta_aux.fechaCreacion = str(oferta_individual["fechaCreacion"])
                oferta_aux.fechaFin = str(oferta_individual["fechaFin"])
                oferta_aux.precio = oferta_individual["precio"]
                oferta_aux.vinculo = oferta_individual["vinculo"]
                oferta_aux.publicador = str(oferta_individual["publicador"])
                oferta_aux.obtener_puntuacion()
                resultado.append(oferta_aux)
        return resultado

    def construir_ruta(self, cantidad_imagenes: int) -> list:
        total_imagenes = self.contar_imagenes()
        lista_rutas = []
        ruta_base = str(self.idPublicacion) + "-"
        indice = 1
        while indice <= cantidad_imagenes:
            lista_rutas.append(ruta_base + str(total_imagenes + indice) + ".png")
            indice += 1

        return lista_rutas


