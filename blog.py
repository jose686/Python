# Description: Este archivo contiene la clase Blog que se encarga de manejar las operaciones de la base de datos



from datetime import datetime
import os
from sqlalchemy import Column, DateTime, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Crear la base de datos

Base = declarative_base()

# Crear la conexión a la base de datos
engine = create_engine("mysql+pymysql://root:1234@localhost/api_py")

# Crear la sesión
Session = sessionmaker(bind=engine)
session = Session()



# Crear la clase Noticia
class Noticia(Base):
    __tablename__ = "noticia"
    id = Column(Integer, primary_key=True)
    titulo = Column(String(250))
    parrafo = Column(Text)
    imagen = Column(String(250))
    created_at = Column(DateTime, default=datetime.now)

    def __str__(self):
        return self.titulo






# Crear la función para registrar una noticia
def registrar(titulo, parrafo, imagen):
    Base.metadata.create_all(engine)
    noticia = Noticia(titulo=titulo, parrafo=parrafo, imagen=imagen)
    session.add(noticia)
    session.commit()

#
def imprimir():
    Base.metadata.create_all(engine)
    #session.commit()
    noticias = session.query(Noticia).order_by(Noticia.created_at.desc()).all()
    return noticias

# Crear la función para borrar una noticia
def borrar_noticia(noticia_id):
    #Base.metadata.create_all(engine)
    noticia = session.query(Noticia).get(noticia_id)
    if noticia:
          # Eliminar la imagen del sistema de archivos
        if noticia.imagen and os.path.exists(noticia.imagen):
            os.remove(noticia.imagen)
        session.delete(noticia)
        session.commit()
        return True
    return False