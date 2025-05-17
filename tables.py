# crear_todas_las_tablas.py

from database.db import Base, engine

# Importa todos los modelos explícitamente
from models.usuario import Usuario
from models.paciente import Paciente
from models.paciente_neonato import PacienteNeonato
from models.medicion import Medicion

# Crear todas las tablas
Base.metadata.create_all(engine)

print("✅ Todas las tablas fueron creadas correctamente.")
