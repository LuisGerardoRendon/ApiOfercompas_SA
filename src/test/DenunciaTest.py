from http import HTTPStatus

import pytest

from src.negocio import Motivo
from src.negocio.Denuncia import Denuncia

denuncia = Denuncia()
denuncia.id_denunciante = 10
denuncia.id_publicacion = 34
denuncia.motivo = Motivo.ALCHOL_TABACO
denuncia.comentario = "Promociona alcohol barato"


def test_registrar():
    resultado = denuncia.registrar()
    assert resultado == HTTPStatus.CREATED


def test_existe_denuncia():
    assert denuncia.existe_denuncia()


def test_text_existe_publicacion():
    assert denuncia.existe_publicacion()

def test_aumnetar_numero_denuncias():
    assert  denuncia.aumentar_numero_denuncias()
