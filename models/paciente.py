from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from database.db import Base
from sqlalchemy import ForeignKey


class Paciente(Base):
    __tablename__ = "pacientes"
    
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255))
    cedula = Column(String(50), unique=True, index=True)
    fecha_nacimiento = Column(Date)
    edad = Column(Integer)

    sexo = Column(String(20))
    telefono = Column(String(20))
    direccion = Column(String(255))


    mediciones = relationship("Medicion", back_populates="paciente")
    usuario = relationship("Usuario", back_populates="pacientes")

