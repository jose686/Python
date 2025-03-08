from datetime import datetime # Importamos la clase 'datetime' de la librería 'datetime'
from sqlalchemy import Column, DateTime, Integer, String # Importamos las clases necesarias de 'sqlalchemy'
from sqlalchemy.orm import sessionmaker
from blog import Base, engine  # Importamos el objeto 'Base' de 'blog.py'
from passlib.hash import sha256_crypt
from werkzeug.security import check_password_hash



# Crear la sesión
Session = sessionmaker(bind=engine)
db_session = Session()  # Cambiar el nombre de la sesión a db_session


# Crear la clase Usuario
class Usuario(Base):
    __tablename__ = "usuario"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(250))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(250), nullable=False)
    rol = Column(String(50), nullable=False, default='usuario')  # Nuevo campo 'rol'
    created_at = Column(DateTime, default=datetime.now)

    def __str__(self):
        return self.nombre
    

# Crear la función para registrar un usuario
def crear_usuario(usuario):
    db_session.add(usuario)
    db_session.commit()
    return  "Usuario creado exitosamente", 201



# Ejemplo de uso  
def obtener_usuarios():
    usuarios = db_session.query(Usuario).all()
    resultado = []
    for usuario in usuarios:
        resultado.append({
        'id': usuario.id,
        'nombre': usuario.nombre,
        'email': usuario.email,
        'rol': usuario.rol,
        'created_at': usuario.created_at
    })  
    return resultado, 200
#print(obtener_usuarios())


# Crear la función para buscar un usuario por email
def buscar_usuario_por_email(email):
    usuario = db_session.query(Usuario).filter_by(email=email).first()
    return usuario  # Retornar el objeto Usuario directamente



# Crear la función para verificar la contraseña
def verificar_password(email, password):
    usuario = buscar_usuario_por_email(email)
    if usuario:
        if sha256_crypt.verify(password, usuario.password):
            return True, usuario
    return False, None

# actualizar contraseña
def actualizar_password(id, nueva_password):
    usuario = db_session.query(Usuario).get(id)
    if not usuario:
        return {"mensaje": "Usuario no encontrado"}, 404

    usuario.password = sha256_crypt.hash(nueva_password)
    db_session.commit()
    return {"mensaje": "Contraseña actualizada exitosamente"}, 200


#id_usuario = 1
#nueva_contraseña = "1234"
#print(actualizar_contraseña(id_usuario, nueva_contraseña))

# Crear la función para eliminar un usuario
def eliminar_usuario(id):
    usuario = db_session.query(Usuario).get(id)
    if not usuario:
        return {"mensaje": "Usuario no encontrado"}, 404

    db_session.delete(usuario)
    db_session.commit()
    return {"mensaje": "Usuario eliminado exitosamente"}, 200

# Ejemplo de uso
#id_usuario = 1
#print(eliminar_usuario(id_usuario))




# Crear la función para generar un hash de la contraseña
def generar_hass(password):
    return sha256_crypt.hash(password)

# Usuario por defecto
usuario_por_defecto = Usuario(
    nombre="admin",
    email="admin@example.com",
    password=generar_hass("admin123"),
    rol="admin"
)

#crear_usuario(usuario_por_defecto)
#db_session.add(usuario_por_defecto)
#db_session.commit()



