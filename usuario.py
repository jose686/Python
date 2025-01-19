
from datetime import datetime # Importamos la clase 'datetime' de la librería 'datetime'
from sqlalchemy import Column, DateTime, Integer, String # Importamos las clases necesarias de 'sqlalchemy'
from blog import Base, session, engine  # Importamos el objeto 'Base' de 'blog.py'
from werkzeug.security import generate_password_hash,check_password_hash



#Session = sessionmaker(bind=engine)




# Crear la clase Usuario
class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    email = Column(String(100),nullable=False,unique=True)
    password = Column(String(250),nullable=False,)
    rol = Column(String(50), nullable=False, default='usuario')  # Nuevo campo 'rol'
    created_at = Column(DateTime, default=datetime.now)

    def __str__(self):
        return self.nombre
    

#Base.metadata.create_all(engine)
#usuario = session.query(Usuario).all()
#Base.metadata.drop_all(engine, tables=[Base.metadata.tables['usuarios']])


# Crear la función para registrar un usuario
def crear_usuario(Usuario):
    session.add(Usuario)
    session.commit()
    return  "Usuario creado exitosamente", 201



# Ejemplo de uso  
def obtener_usuarios():
    usuarios = session.query(Usuario).all()
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
    usuario = session.query(Usuario).filter_by(email=email).first()
    if usuario:
        resultado = {
            'id': usuario.id,
            'nombre': usuario.nombre,
            'email': usuario.email,
            'rol': usuario.rol,
            'created_at': usuario.created_at
        }
        return resultado
    else:
        return {"mensaje": "Usuario no encontrado"}, 404

# Ejemplo de uso
#email_a_buscar = "admin@example.com"
#print(buscar_usuario_por_email(email_a_buscar))

# Crear la función para verificar la contraseña
def verificar_password(email, password):
    usuario = session.query(Usuario).filter_by(email=email).first()
    if not usuario:
        return False, {"mensaje": "Usuario no encontrado"}

    if check_password_hash(usuario.password, password):
        return True, usuario
    else:
        return False, {"mensaje": "Contraseña incorrecta"}

# actualizar contraseña
def actualizar_password(id, nueva_password):
    usuario = session.query(Usuario).get(id)
    if not usuario:
        return {"mensaje": "Usuario no encontrado"}, 404

    usuario.password = generate_password_hash(nueva_password)
    session.commit()
    return {"mensaje": "Contraseña actualizada exitosamente"}, 200


#id_usuario = 1
#nueva_contraseña = "1234"
#print(actualizar_contraseña(id_usuario, nueva_contraseña))

# Crear la función para eliminar un usuario
def eliminar_usuario(id):
    usuario = session.query(Usuario).get(id)
    if not usuario:
        return {"mensaje": "Usuario no encontrado"}, 404

    session.delete(usuario)
    session.commit()
    return {"mensaje": "Usuario eliminado exitosamente"}, 200

# Ejemplo de uso
#id_usuario = 1
#print(eliminar_usuario(id_usuario))




# Crear la función para generar un hash de la contraseña
def generar_hass(password):
    return generate_password_hash(password)

# Usuario por defecto
usuario_por_defecto = Usuario(
    nombre="admin",
    email="admin@example.com",
    password=generar_hass("admin123"),
    rol="admin"
)

#crear_usuario(usuario_por_defecto)
#session.add(usuario_por_defecto)
#session.commit()



