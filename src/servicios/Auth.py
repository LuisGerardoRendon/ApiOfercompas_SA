from datetime import datetime
from functools import update_wrapper
from typing import Any

from cryptography.fernet import Fernet, InvalidToken
from flask import session, Response, request

from src.negocio.CodigosRespuesta import NO_AUTORIZADO, PROHIBIDO, SESION_EXPIRADA
from src.negocio.MiembroOfercompas import MiembroOfercompas


class Auth:
    secret_password: bytes = None

    @staticmethod
    def set_password():
        Auth.secret_password = Fernet.generate_key()

    @staticmethod
    def requires_token(operation):
        def verify_auth(*args, **kwargs):
            token = request.headers.get("token")
            saved_token = None
            try:
                saved_token = session["token"]
                if token is not None and saved_token is not None and token == saved_token:
                    session.modified = True
                    response = operation(*args, **kwargs)
                else:
                    response = Response(status=NO_AUTORIZADO)
            except KeyError:
                if token is not None and saved_token is None:
                    response = Response(status=SESION_EXPIRADA)
                else:
                    response = Response(status=NO_AUTORIZADO)
            return response

        return update_wrapper(verify_auth, operation)

    @staticmethod
    def requires_role(role: Any):
        def decorator(operation):
            def verify_role(*args, **kwargs):
                token = request.headers.get("token")
                if token is not None:
                    values = Auth.decode_token(token)
                    if str(values["tipo_miembro"]) == str(role):
                        response = operation(*args, **kwargs)
                    else:
                        response = Response(status=PROHIBIDO)
                else:
                    response = Response(status=PROHIBIDO)
                return response

            return update_wrapper(verify_role, operation)

        return decorator

    @staticmethod
    def verificar_autor(idPublicador, token):
        response = None
        if token is not None:
            try:
                values = Auth.decode_token(token)
                response = str(values["id_miembro"]) == str(idPublicador)
            except InvalidToken:
                pass
            return response

    @staticmethod
    def generate_token(miembro_ofercompas: MiembroOfercompas) -> str:
        if Auth.secret_password is None:
            Auth.set_password()
        timestamp = datetime.now().strftime("%H:%M:%S")
        value: str = miembro_ofercompas.email + "/"
        value += miembro_ofercompas.contrasenia + "/"
        value += str(int(miembro_ofercompas.tipoMiembro)) + "/"
        value += str(int(miembro_ofercompas.idMiembro)) + "/"
        value += timestamp
        return Auth.encode(value, Auth.secret_password)

    @staticmethod
    def decode_token(token: str) -> dict:
        if Auth.secret_password is None:
            Auth.set_password()
        decoded_token = Auth.decode(token, Auth.secret_password)
        decoded_token = decoded_token.split("/")
        return {
            "email": decoded_token[0],
            "contrasenia": decoded_token[1],
            "tipo_miembro": decoded_token[2],
            "id_miembro": decoded_token[3]
        }

    @staticmethod
    def decode(value: str, key: bytes) -> str:
        return Fernet(key).decrypt(value.encode()).decode()

    @staticmethod
    def encode(value: str, key: bytes) -> str:
        return Fernet(key).encrypt(value.encode()).decode()
