import json
from http import HTTPStatus

from flask import Blueprint, request, Response

from src.negocio.Oferta import Oferta
from src.servicios.Auth import Auth
from src.transferencia_archivos.ServidorArchivos import ServidorArchivos

rutas_oferta = Blueprint("rutas_oferta", __name__)


@rutas_oferta.route("/ofertas/<id_publicacion>/imagenes", methods=["POST"])
def registrar_imagen(id_publicacion):
    status = HTTPStatus.BAD_REQUEST
    imagenes = []
    for imagen in request.files.getlist("imagenes"):
        imagenes.append(imagen)

    oferta = Oferta()
    oferta.idPublicacion = id_publicacion
    rutas = oferta.construir_rutas(len(imagenes))
    servidor = ServidorArchivos()
    resultado = 0
    indice = 0
    while indice < len(imagenes) and resultado == 0:
        resultado = servidor.guardar_archivo(imagenes[indice], rutas[indice])
        if resultado == 0:
            oferta.registrar_imagen(rutas[indice])
        indice += 1
    status = HTTPStatus.CREATED
    respuesta = Response(
        oferta.convertir_a_json(),
        status=status,
        mimetype="application/json"
    )
    return respuesta


@rutas_oferta.route("/ofertas", methods=["POST"])
def registrar_oferta():
    oferta_recibida = request.json
    valores_requeridos = {"titulo", "descripcion", "precio", "fechaCreacion", "fechaFin", "publicador", "categoria",
                          "vinculo"}
    respuesta = Response(status=HTTPStatus.BAD_REQUEST)
    if oferta_recibida is not None:
        if all(llave in oferta_recibida for llave in valores_requeridos):
            oferta = Oferta()
            oferta.titulo = oferta_recibida["titulo"]
            oferta.descripcion = oferta_recibida["descripcion"]
            oferta.fechaCreacion = oferta_recibida["fechaCreacion"]
            oferta.fechaFin = oferta_recibida["fechaFin"]
            oferta.categoria = oferta_recibida["categoria"]
            oferta.publicador = oferta_recibida["publicador"]
            oferta.precio = oferta_recibida["precio"]
            oferta.vinculo = oferta_recibida["vinculo"]
            status = oferta.registrar_oferta()
            if status == HTTPStatus.CREATED:
                respuesta = Response(
                    json.dumps(oferta.convertir_a_json()),
                    status=status,
                    mimetype="application/json"
                )
            else:
                respuesta = Response(status=status)
        else:
            respuesta = Response(status=HTTPStatus.BAD_REQUEST)
    else:
        respuesta = Response(status=HTTPStatus.BAD_REQUEST)

    return respuesta


@rutas_oferta.route("/ofertas/<idPublicacion>", methods=["PUT"])
def actualizar_oferta(idPublicacion):
    print("IDDDDD")
    print(idPublicacion)
    oferta_recibida = request.json
    valores_requeridos = {"titulo", "descripcion", "precio", "fechaCreacion", "fechaFin", "categoria", "vinculo"}
    respuesta = Response(status=HTTPStatus.BAD_REQUEST)
    if oferta_recibida is not None:
        if all(llave in oferta_recibida for llave in valores_requeridos):
            oferta = Oferta()
            oferta.idPublicacion = idPublicacion
            oferta.titulo = oferta_recibida["titulo"]
            oferta.descripcion = oferta_recibida["descripcion"]
            oferta.fechaCreacion = oferta_recibida["fechaCreacion"]
            oferta.fechaFin = oferta_recibida["fechaFin"]
            oferta.categoria = oferta_recibida["categoria"]
            oferta.precio = oferta_recibida["precio"]
            oferta.vinculo = oferta_recibida["vinculo"]
            oferta.obtener_autor_por_id()
            status = oferta.actualizar_oferta(idPublicacion)
            if status == HTTPStatus.OK:
                respuesta = Response(
                    json.dumps(oferta.convertir_a_json()),
                    status=status,
                    mimetype="application/json"
                )
            else:
                respuesta = Response(status=status)

        else:
            respuesta = Response(status=HTTPStatus.BAD_REQUEST)

    return respuesta

@rutas_oferta.route("/ofertas", methods=["GET"])
def obtener_oferta():
    pagina = request.args.get("pagina", default=1, type=int)
    categoria = request.args.get("categoria", default=-1, type=int)
    id_publicador = request.args.get("idPublicador", default=0, type=int)
    if id_publicador != 0:
        ofertas = Oferta.obtener_por_id_publicador(pagina, id_publicador)
    else:
        ofertas = Oferta.obtener_oferta(pagina, categoria)
    if ofertas:
        ofertas_jsons = []
        for oferta in ofertas:
            print(oferta.titulo)
            ofertas_jsons.append(oferta.convertir_a_json())
        respuesta = Response(json.dumps(ofertas_jsons), status=HTTPStatus.OK, mimetype="application/json")
    else:
        respuesta = Response(status=HTTPStatus.NOT_FOUND)
    return respuesta




