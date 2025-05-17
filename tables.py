from database.db import engine, Base
from models.usuario import Usuario

Base.metadata.create_all(bind=engine)

print("¡Tablas creadas exitosamente!")
