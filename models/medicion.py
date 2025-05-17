from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base
from sqlalchemy import Column, Integer, Float, Date, ForeignKey, String

class Medicion(Base):
    __tablename__ = "mediciones"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    patient_id = Column(String(50), ForeignKey("pacientes.cedula"))
    height = Column(Float)
    weight = Column(Float)
    waist = Column(Float)
    hip = Column(Float)
    triceps = Column(Float)
    subscapular = Column(Float)

    paciente = relationship("Paciente", back_populates="mediciones")
