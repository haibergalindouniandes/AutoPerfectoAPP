# Import de librerias
from sqlalchemy import Column, Integer, Float, Date, ForeignKey

from src.modelo.automovil import Automovil
from src.modelo.mantenimiento import Mantenimiento
from .declarative_base import Base, relationship

# Clase que contiene la estructura de la tabla Mantenimiento
class Accion(Base):
    __tablename__ = 'accion'

    id = Column(Integer, primary_key=True)
    kilometraje = Column(Float)
    valor = Column(Float)
    fecha = Column(Date)
    mantenimiento_id = Column(Integer, ForeignKey(Mantenimiento.id, ondelete="cascade", onupdate="cascade"), nullable=False)
    mantenimiento = relationship(Mantenimiento, uselist=False)
    automovil_id = Column(Integer, ForeignKey(Automovil.id, ondelete="cascade", onupdate="cascade"), nullable=False)
    automovil = relationship(Automovil, uselist=False)
    

    def __init__(self, kilometraje, valor, fecha, mantenimiento_id, automovil_id):
            self.kilometraje = kilometraje
            self.valor = valor
            self.fecha = fecha
            self.mantenimiento_id = mantenimiento_id
            self.automovil_id = automovil_id