from http import HTTPStatus
import pytest

from src.negocio.Comentario import Comentario

comentario = Comentario()
comentario.id_publicacion = 1
comentario.id_miembro = 1
comentario.contenido = "Este es el primer comentario de ofercompas gg"

def test_registrar():
    resultado = comentario.registrar()
    assert resultado == HTTPStatus.CREATED

def test_obtener_comentarios():
    resultado = Comentario.obtener_comentarios(32)
    assert resultado
