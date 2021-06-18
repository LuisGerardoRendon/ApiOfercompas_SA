import pytest

from src.negocio import CodigosRespuesta, TipoMiembro
from src.negocio.MiembroOfercompas import MiembroOfercompas

miembro = MiembroOfercompas()
miembro.email = "nuevoMiembro@gmail.com"
miembro.tipoMiembro = TipoMiembro.COMUN
miembro.nickname = "nuevoMiembro"
miembro.contrasenia = "123456"


def test_email_registrado():
    miembro.email = "edsonsito@gmail.com"
    resultado = miembro.email_registrado()
    assert resultado


def test_nickname_registrado():
    miembro.nickname = "MtroOcharan"
    resultado = miembro.nickname_registrado()
    assert resultado


def test_registrar():
    resultado = miembro.registrar()
    assert resultado == CodigosRespuesta.RECURSO_CREADO or resultado == CodigosRespuesta.CONFLICTO


def test_actualizar_miembro():
    miembro.nickname = "Jorge Manuel"
    miembro.email = "jorgemanuel@gmail.com"
    resultado = miembro.actualizar("pepsi@gmail.com")
    assert resultado == CodigosRespuesta.OK


def test_get_id():
    miembro.email = "jorgemanuel@gmail.com"
    id_miembro = miembro.getId()
    id_esperado = 11
    assert id_miembro == id_esperado


def test_iniciar_sesion():
    miembroConSesion = MiembroOfercompas()
    miembroConSesion.email = "efrainrazziel@gmail.com"
    miembroConSesion.contrasenia = "beethoven"
    respuesta = miembroConSesion.iniciar_sesion()
    valores_llenados = False
    if miembroConSesion.idMiembro is not None and miembroConSesion.nickname is not None and miembroConSesion.tipoMiembro is not None:
        valores_llenados = True
    assert valores_llenados and respuesta == CodigosRespuesta.OK

def test_obtener_reporte():
    reporte = MiembroOfercompas.obtener_reporte(26)
    puntuacion = reporte.get("puntuacionTotal")
    assert puntuacion >= 0