# Import de librerias
from sqlalchemy import Column, Integer, String
from .declarative_base import Base

# Clase que contiene la estructura de la tabla Mantenimiento
class Mantenimiento(Base):
    __tablename__ = 'mantenimiento'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    descripcion = Column(String)

    def __init__(self, nombre, descripcion):
            self.nombre = nombre
            self.descripcion = descripcion