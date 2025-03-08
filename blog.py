# Description: Este archivo contiene la clase Blog que se encarga de manejar las operaciones de la base de datos

from datetime import datetime
import os
from sqlalchemy import Column, DateTime, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask import jsonify  # Importar jsonify desde flask


# Crear la base de datos

Base = declarative_base()

# Crear la conexión a la base de datos
engine = create_engine("mysql+pymysql://root:1234@localhost/api_py")

# Crear la sesión
Session = sessionmaker(bind=engine)
db_session = Session()  # Cambiar el nombre de la sesión a db_session



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
    db_session.add(noticia)  # Utilizar db_session en lugar de session
    db_session.commit()  # Utilizar db_session en lugar de session

# Crear la función para imprimir las noticias
def imprimir():
    Base.metadata.create_all(engine)
    #db_session.commit()
    noticias = db_session.query(Noticia).order_by(Noticia.created_at.desc()).all()
    return noticias



# Crear la función para imprimir las noticias
def imprimir_noticias_admin():
    Base.metadata.create_all(engine)
    noticias = db_session.query(Noticia).order_by(Noticia.created_at.desc()).all()
    
    # Convertir los objetos Noticia a un formato JSON serializable
    noticias_lista = []
    for noticia in noticias:
        noticias_lista.append({
            'id': noticia.id,
            'titulo': noticia.titulo,
            'parrafo': noticia.parrafo,
            'imagen': noticia.imagen,
            'created_at': noticia.created_at.isoformat()  # Convertir a formato ISO para JSON
        })
    
    return jsonify(noticias_lista)

# Crear la función para borrar una noticia
def borrar_noticia(noticia_id):
    #Base.metadata.create_all(engine)
    noticia = db_session.query(Noticia).get(noticia_id)  # Utilizar db_session en lugar de session
    if noticia:
          # Eliminar la imagen del sistema de archivos
        if noticia.imagen and os.path.exists(noticia.imagen):
            os.remove(noticia.imagen)
        db_session.delete(noticia)  # Utilizar db_session en lugar de session
        db_session.commit()  # Utilizar db_session en lugar de session
        return True
    return False



