from sqlalchemy import Column, Integer, String, Date, Boolean
from database.db import Base
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


class PacienteNeonato(Base):
    __tablename__ = "pacientes_neonatos"

    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255))
    numero_identificacion = Column(String(50), unique=True,index = True)  # Nuevo campo
    fecha_nacimiento = Column(Date)
    edad_semanas = Column(Integer)      # Edad gestacional al nacer
    prematuro = Column(Boolean)
    sexo = Column(String(20))
    peso = Column(Integer)
    talla = Column(Integer)
    pc = Column(Integer)
    clasificacion_peso = Column(String(10))

    usuario = relationship("Usuario", back_populates="pacientes_neonatos", lazy="joined")


PacienteNeonato.__table__