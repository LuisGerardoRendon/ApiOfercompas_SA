from thrift.protocol.TBinaryProtocol import TBinaryProtocol
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from werkzeug.datastructures import FileStorage

from src.transferencia_archivos.OfercompasArchivos.ServicioDeAlmacenamiento import Client
from src.transferencia_archivos.OfercompasArchivos.ttypes import Imagen


class ServidorArchivos:
    host = "localhost"
    puerto = 42778

    def __init__(self):
        socket = TSocket(self.host, self.puerto)
        self.transport = TBufferedTransport(socket)
        protocolo = TBinaryProtocol(self.transport)
        self.conexion = Client(protocolo)

    def guardar_archivo(self, archivo: FileStorage, ruta: str):
        imagen = Imagen(archivo.read(), ruta)
        self.transport.open()
        resultado = self.conexion.guardarArchivo(imagen)
        self.transport.close()
        return resultado

    def eliminar_archivo(self, ruta: str):
        self.transport.open()
        resultado = self.conexion.eliminarArchivo(ruta)
        self.transport.close()
        return resultado

    def obtener_archivos(self, ruta: str) -> list:
        print(ruta)
        self.transport.open()
        resultado = self.conexion.obtenerArchivos(ruta)
        self.transport.close()
        return resultado
