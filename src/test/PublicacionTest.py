from src.negocio.Publicacion import Publicacion


def test_obtener_ofertas_denunciadas():
    resultado = Publicacion.obtener_publicaciones_denunciadas(1)
    print(resultado[0].titulo)
    assert resultado
