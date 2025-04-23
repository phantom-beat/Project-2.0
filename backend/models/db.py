
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URI = 'mysql+pymysql://usuario:contraseña@localhost/nutriclinic'

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()
