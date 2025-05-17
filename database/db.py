from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


USER = 'root'          
PASSWORD = 'root'  
HOST = 'localhost'      
PORT = '3306'           
DATABASE = 'nutriclincIMB' 

# Cadena de conexión
DATABASE_URL = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'

# Motor de conexión
engine = create_engine(DATABASE_URL, echo=True)

# Sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()
