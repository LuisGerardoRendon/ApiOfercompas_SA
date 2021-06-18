import json
from http import HTTPStatus

from flask import Blueprint, request, Response

from src.negocio.CodigosRespuesta import MALA_SOLICITUD, RECURSO_CREADO, OK
from src.negocio.CodigoDescuento import CodigoDescuento
from src.servicios.Auth import Auth

rutas_codigo = Blueprint("rutas_codigo", __name__)


@rutas_codigo.route("/codigos", methods=["POST"])
def registrar_codigo():
    codigo_recibido = request.json
    valores_requeridos = {"titulo", "descripcion", "codigo", "fechaCreacion", "fechaFin", "publicador", "categoria"}
    respuesta = Response(status=MALA_SOLICITUD)
    if codigo_recibido is not None:
        if all(llave in codigo_recibido for llave in valores_requeridos):
            codigo_descuento = CodigoDescuento()
            codigo_descuento.titulo = codigo_recibido["titulo"]
            codigo_descuento.descripcion = codigo_recibido["descripcion"]
            codigo_descuento.fechaCreacion = codigo_recibido["fechaCreacion"]
            codigo_descuento.fechaFin = codigo_recibido["fechaFin"]
            codigo_descuento.categoria = codigo_recibido["categoria"]
            codigo_descuento.publicador = codigo_recibido["publicador"]
            codigo_descuento.codigo = codigo_recibido["codigo"]
            status = codigo_descuento.registrar_codigo()
            if status == RECURSO_CREADO:
                respuesta = Response(
                    json.dumps({
                        "idPublicacion": codigo_descuento.idPublicacion,
                        "titulo": codigo_descuento.titulo,
                        "descripcion": codigo_descuento.descripcion,
                        "fechaCreacion": codigo_descuento.fechaCreacion,
                        "fechaFin": codigo_descuento.fechaFin,
                        "publicador": codigo_descuento.publicador,
                        "codigo": codigo_descuento.codigo
                    }),
                    status=status,
                    mimetype="application/json"
                )
            else:
                respuesta = Response(status=status)
        else:
            respuesta = Response(status=MALA_SOLICITUD)

    return respuesta


@rutas_codigo.route("/codigos/<idPublicacion>", methods=["PUT"])
def actualizar_codigo(idPublicacion):
    codigo_recibido = request.json
    valores_requeridos = {"titulo", "descripcion", "codigo", "fechaCreacion", "fechaFin", "categoria"}
    respuesta = Response(status=MALA_SOLICITUD)
    if codigo_recibido is not None:
        if all(llave in codigo_recibido for llave in valores_requeridos):
            codigo_descuento = CodigoDescuento()
            codigo_descuento.idPublicacion = idPublicacion
            codigo_descuento.titulo = codigo_recibido["titulo"]
            codigo_descuento.descripcion = codigo_recibido["descripcion"]
            codigo_descuento.fechaCreacion = codigo_recibido["fechaCreacion"]
            codigo_descuento.fechaFin = codigo_recibido["fechaFin"]
            codigo_descuento.categoria = codigo_recibido["categoria"]
            codigo_descuento.codigo = codigo_recibido["codigo"]
            status = codigo_descuento.actualizar_codigo(idPublicacion)

            token = request.headers.get("token")
            if status == HTTPStatus.OK:
                respuesta = Response(
                    json.dumps(codigo_descuento.convertir_a_json()),
                    status=status,
                    mimetype="application/json"
                )
            else:
                respuesta = Response(status=status)
        else:
            respuesta = Response(status=MALA_SOLICITUD)

    return respuesta


@rutas_codigo.route("/codigos", methods=["GET"])
def obtener_codigo():
    pagina = request.args.get("pagina", default=1, type=int)
    categoria = request.args.get("categoria", default=-1, type=int)
    id_publicador = request.args.get("idPublicador", default=0, type=int)
    if id_publicador != 0:
        codigos = CodigoDescuento.obtener_por_id_publicador(pagina, id_publicador)
    else:
        codigos = CodigoDescuento.obtener_codigo(pagina, categoria)
    if codigos:
        codigos_jsons = []
        for codigo in codigos:
            codigos_jsons.append(codigo.convertir_a_json())
        prueba = json.dumps(codigos_jsons)
        print(prueba)
        respuesta = Response(json.dumps(codigos_jsons), status=HTTPStatus.OK, mimetype="application/json")
    else:
        respuesta = Response(status=HTTPStatus.NOT_FOUND)
    return respuesta
