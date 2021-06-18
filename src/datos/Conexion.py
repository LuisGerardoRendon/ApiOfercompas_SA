from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()


class Conexion(Base):
    __abstract__ = True

    @staticmethod
    def abrir_conexion() -> Session:
        engine = create_engine("mysql+pymysql://amigo:beethoven@ofercompas.ddns.net/Ofercompas")
        return Session(engine)
