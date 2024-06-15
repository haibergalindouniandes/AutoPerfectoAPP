# Import de librerias
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///auto_perfecto_db.sqlite')
Session = sessionmaker(bind=engine)
Base = declarative_base()
session = Session()

#Forzar restricciones de llaves foraneas
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()