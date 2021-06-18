import json
from http import HTTPStatus
from flask import Blueprint, request, Response, session
from src.negocio import CodigosRespuesta, TipoMiembro
from src.negocio.MiembroOfercompas import MiembroOfercompas
from src.servicios.Auth import Auth

rutas_miembro = Blueprint("rutas_miembro", __name__)

@rutas_miembro.route("/miembros", methods=["POST"])
def registrar_miembro():
    miembro_recibido = request.json
    valores_requeridos = {"email", "nickname", "contrasenia"}
    respuesta = Response(status=CodigosRespuesta.MALA_SOLICITUD)
    if miembro_recibido is not None:
        if all(llave in miembro_recibido for llave in valores_requeridos):
            miembro = MiembroOfercompas()
            miembro.instanciar_con_hashmap(miembro_recibido)
            resultado = miembro.registrar()
            if resultado == CodigosRespuesta.RECURSO_CREADO:
                respuesta = Response(
                    miembro.hacer_json(),
                    status=CodigosRespuesta.RECURSO_CREADO,
                    mimetype="application/json"
                )
            elif resultado == CodigosRespuesta.ERROR_INTERNO:
                respuesta = Response(status=CodigosRespuesta.ERROR_INTERNO)
            elif resultado == CodigosRespuesta.CONFLICTO:
                respuesta = Response(status=CodigosRespuesta.CONFLICTO)

    else:
        respuesta = Response(status=CodigosRespuesta.MALA_SOLICITUD)

    return respuesta


@rutas_miembro.route("/miembros/<old_email>", methods=["PUT"])
def actualizar_miembro(old_email):
    valores_requeridos = {"email", "nickname", "contrasenia"}
    miembro_recibido = request.json
    print(miembro_recibido)
    respuesta = Response(CodigosRespuesta.MALA_SOLICITUD)
    if all(llave in miembro_recibido for llave in valores_requeridos):
        miembro = MiembroOfercompas()
        miembro.instanciar_con_hashmap(miembro_recibido)
        resultado = miembro.actualizar(old_email)
        if resultado == CodigosRespuesta.OK:
            respuesta = Response(
                miembro.hacer_json(),
                status=CodigosRespuesta.OK,
                mimetype="application/json"
            )
        elif resultado == CodigosRespuesta.ERROR_INTERNO:
            respuesta = Response(status=CodigosRespuesta.ERROR_INTERNO)
        elif resultado == CodigosRespuesta.CONFLICTO:
            respuesta = Response(status=CodigosRespuesta.CONFLICTO)

    else:
        respuesta = Response(status=400)
    return respuesta


@rutas_miembro.route("/miembros", methods=["GET"])
def getprueba():
    respuesta = Response(
        json.dumps({
            "idMiembro": "Efrain",
            "email": "Razziel",
            "contrasenia": "Arenas",
            "nickname": "Ramirez",
            "estado": "Sexto",
            "tipoMiembro": "Semestre234"
        }),
        status=200,
        mimetype="application/json"
    )
    return respuesta


@rutas_miembro.route("/login", methods=["POST"])
def iniciar_sesion():
    valores_requeridos = {"email", "contrasenia"}
    miembro_recibido = request.json
    respuesta = Response(CodigosRespuesta.MALA_SOLICITUD)
    if all(llave in miembro_recibido for llave in valores_requeridos):
        miembro = MiembroOfercompas()
        miembro.email = miembro_recibido["email"]
        miembro.contrasenia = miembro_recibido["contrasenia"]

        resultado = miembro.iniciar_sesion()
        if resultado == CodigosRespuesta.OK:
            token = Auth.generate_token(miembro)
            session.permanent = True
            session["token"] = token
            miembro_json = miembro.hacer_json_token(token)

            respuesta = Response(
                miembro_json,
                status=CodigosRespuesta.OK,
                mimetype="application/json"

            )
        else:
            respuesta = Response(status=resultado)
    else:
        respuesta = Response(status=CodigosRespuesta.MALA_SOLICITUD)
    return respuesta


@rutas_miembro.route("/miembros/reportes", methods=["GET"])
def obtener_miembros_mas_denunciados():
    respuesta = Response(CodigosRespuesta.NO_ENCONTRADO)
    miembrosDenunciados = MiembroOfercompas.obtener_miembros_mas_denunciados()
    if miembrosDenunciados:
        respuesta = Response(
            json.dumps(miembrosDenunciados),
            status=HTTPStatus.OK,
            mimetype="application/json"
        )
    return respuesta


@rutas_miembro.route("/miembros/<id_miembro>/reporte", methods=["GET"])
def obtener_reporte_miembro(id_miembro):
    respuesta = Response(HTTPStatus.INTERNAL_SERVER_ERROR)
    reporte = MiembroOfercompas.obtener_reporte(id_miembro)
    respuesta = Response(
        json.dumps(reporte),
        status=HTTPStatus.OK,
        mimetype="application/json"
    )
    return respuesta


@rutas_miembro.route("/miembros/<id_miembro>/expulsion", methods=["PUT"])
def expulsar_miembro(id_miembro):
    miembro = MiembroOfercompas()
    miembro.idMiembro = id_miembro
    retorno = miembro.expulsar()
    respuesta = Response(status= retorno)
    return respuesta
