import io
import json
from http import HTTPStatus

from flask import Blueprint, Response, request
from src.negocio.Comentario import Comentario
from src.negocio.Denuncia import Denuncia
from src.negocio.Publicacion import Publicacion
from src.negocio.Puntuacion import Puntuacion
from src.servicios.Auth import Auth


rutas_publicacion = Blueprint("rutas_publicacion", __name__)


@rutas_publicacion.route("/publicaciones/<idPublicacion>", methods=["DELETE"])
def eliminar_publicacion(idPublicacion):
    publicacion = Publicacion()
    publicacion.idPublicacion = idPublicacion
    publicacion.obtener_autor_por_id()
    status = Publicacion.eliminar_publicacion(idPublicacion)
    return Response(status=status)


@rutas_publicacion.route("/publicaciones/<idPublicacion>/prohibir", methods=["DELETE"])
def prohibir_publicacion(idPublicacion):
    status = Publicacion.prohibir_publicacion(idPublicacion)
    return Response(status=status)


@rutas_publicacion.route("/publicaciones/<idPublicacion>/puntuaciones", methods=["POST"])
def puntuar_publicacion(idPublicacion):
    puntuacion_recibida = request.json
    valores_requeridos = {"idMiembro", "esPositiva"}
    respuesta = Response(status=HTTPStatus.BAD_REQUEST)
    if puntuacion_recibida is not None:
        if all(llave in puntuacion_recibida for llave in valores_requeridos):
            puntuacion = Puntuacion()
            puntuacion.instanciar_con_hashmap(puntuacion_recibida, idPublicacion)
            resultado = puntuacion.puntuar_publicacion()
            if resultado == HTTPStatus.CREATED:
                respuesta = Response(puntuacion.convertir_a_json(),
                                     status=resultado,
                                     mimetype="application/json")
            else:
                respuesta = Response(status=resultado)
    return respuesta


@rutas_publicacion.route("/publicaciones/<idPublicacion>/interaccion", methods=["GET"])
def obtener_interaccion(idPublicacion):
    respuesta = Response(status=HTTPStatus.OK)
    id_miembro_recibido = int(request.headers.get("idMiembro"))
    print("OBTENIENDO INTERACCION")
    if id_miembro_recibido is not None:
        id_miembro = id_miembro_recibido
        respuesta = Response(json.dumps(Publicacion.obtener_interaccion(id_miembro, idPublicacion)),
                             status=HTTPStatus.OK, mimetype="application/json")
    else:
        respuesta = Response(status=HTTPStatus.NOT_FOUND)
    return respuesta


@rutas_publicacion.route("/publicaciones/<id_publicacion>/comentarios", methods=["POST"])
def registrar_comentario(id_publicacion):
    comentario_recibido = request.json
    valores_requeridos = {"idMiembro", "contenido"}
    print(comentario_recibido)
    respuesta = Response(status=HTTPStatus.BAD_REQUEST)
    if comentario_recibido is not None:
        if all(llave in comentario_recibido for llave in valores_requeridos):
            comentario = Comentario()
            comentario.instanciar_con_hashmap(comentario_recibido, id_publicacion)
            resultado = comentario.registrar()
            if resultado == HTTPStatus.CREATED:
                respuesta = Response(comentario.hacer_json_sin_nickname(),
                                     status=resultado,
                                     mimetype="application/json")

            else:
                respuesta = Response(status=resultado)
    return respuesta


@rutas_publicacion.route("/publicaciones/<id_publicacion>/comentarios", methods=["GET"])
def obtener_comentarios(id_publicacion):
    respuesta = Response(status=HTTPStatus.BAD_REQUEST)
    if id_publicacion is not None:
        comentarios = Comentario.obtener_comentarios(id_publicacion)
        if comentarios:
            array_comentarios = []
            for comentario in comentarios:
                array_comentarios.append(comentario.hacer_json_nickname_contenido())
            comentarios_json = json.dumps(array_comentarios)
            print(comentarios_json)
            respuesta = Response(comentarios_json, status=HTTPStatus.OK, mimetype="application/json")
        else:
            respuesta = Response(status=HTTPStatus.NOT_FOUND)
    return respuesta


@rutas_publicacion.route("/publicaciones/<id_publicacion>/denuncias", methods=["POST"])
def registrar_denuncia(id_publicacion):
    denuncia_recibida = request.json
    valores_requeridos = {"idDenunciante", "comentario", "motivo"}
    print(denuncia_recibida)
    respuesta = Response(status=HTTPStatus.BAD_REQUEST)
    if denuncia_recibida is not None:
        if all(llave in denuncia_recibida for llave in valores_requeridos):
            denuncia = Denuncia()
        denuncia.instanciar_con_hashmap(denuncia_recibida, id_publicacion)
        resultado = denuncia.registrar()
        if resultado == HTTPStatus.CREATED:
            respuesta = Response(denuncia.hacer_json(),
                                 status=resultado,
                                 mimetype="application/json")

        else:
            respuesta = Response(status=resultado)
    return respuesta

@rutas_publicacion.route("/publicaciones/free", methods =["GET"])
def metodo_default():
    return Response(status=200)