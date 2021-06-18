import io
from http import HTTPStatus

from flask import Blueprint, Response, request, send_file

from src.negocio.Multimedia import Multimedia
from src.negocio.Publicacion import Publicacion
from src.servicios.Auth import Auth
from src.transferencia_archivos.ServidorArchivos import ServidorArchivos

rutas_multimedia = Blueprint("rutas_multimedia", __name__)


@rutas_multimedia.route("/publicaciones/<idPublicacion>/multimedia", methods=["POST"])
def publicar_archivo(idPublicacion):
    print(request.files)
    archivo = request.files.getlist("archivo")[0]
    respuesta = Response(status=HTTPStatus.BAD_REQUEST)
    multimedia = Multimedia()
    servidor = ServidorArchivos()
    resultado = 0
    if archivo.content_type == "image/png" or archivo.content_type == "image/jpeg":
        ruta = str(idPublicacion + "-" + archivo.filename)
        resultado = servidor.guardar_archivo(archivo, ruta)
        if resultado == 0:
            multimedia.registrar_imagen(ruta, idPublicacion)
            respuesta = Response(status=HTTPStatus.CREATED)
    else:
        ruta = str(idPublicacion + "-" + archivo.filename)
        resultado = servidor.guardar_archivo(archivo, ruta)
        if resultado == 0:
            multimedia.registrar_video(ruta, idPublicacion)
            respuesta = Response(status=HTTPStatus.CREATED)

    return respuesta


@rutas_multimedia.route("/publicaciones/<idPublicacion>/imagenes", methods=["GET"])
def recuperar_imagen(idPublicacion):
    multimedia = Multimedia()
    response = Response(status=HTTPStatus.NOT_FOUND)
    ruta_foto = multimedia.obtener_ruta_foto_id(idPublicacion)
    if ruta_foto != "not":
        resultado = multimedia.recuperar_archivo(ruta_foto)
        if resultado:
            response = send_file(
                io.BytesIO(resultado),
                mimetype="image/png",
                as_attachment=False)

    return response


@rutas_multimedia.route("/publicaciones/<idPublicacion>/videos", methods=["GET"])
def recuperar_video(idPublicacion):
    multimedia = Multimedia()
    response = Response(status=HTTPStatus.NOT_FOUND)
    ruta_video = multimedia.obtener_ruta_video_id(idPublicacion)
    if ruta_video != "not":
        resultado = multimedia.recuperar_archivo(ruta_video)
        if resultado:
            response = send_file(
                io.BytesIO(resultado),
                mimetype="video/mp4",
                as_attachment=False)

    return response


@rutas_multimedia.route("/publicaciones/<idPublicacion>/multimedia", methods=["PUT"])
def actualizar_archivo(idPublicacion):
    archivo = request.files.getlist("archivo")[0]
    respuesta = Response(status=HTTPStatus.BAD_REQUEST)
    multimedia = Multimedia()
    servidor = ServidorArchivos()

    resultado = 0
    ruta = str(idPublicacion + "-" + archivo.filename)
    resultado = servidor.guardar_archivo(archivo, ruta)
    if resultado == 0:
        if archivo.content_type == "image/png" or archivo.content_type == "image/jpeg":
            multimedia.actualizar_imagen(ruta, idPublicacion)
            respuesta = Response(status=HTTPStatus.OK)
        else:
            multimedia.actualizar_video(ruta, idPublicacion)
            respuesta = Response(status=HTTPStatus.OK)
    return respuesta
