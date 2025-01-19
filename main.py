"""
Esta es la parte principal de la aplicacion, aqui se encuentran las rutas de la aplicacion
"""


import datetime
from flask import Flask, render_template, request, redirect, session
import os

from blog import borrar_noticia, imprimir, registrar
from tamano_imagen import tamano_img
from usuario import Usuario, buscar_usuario_por_email, crear_usuario, generar_hass, verificar_password

# Crear la aplicación
app = Flask(__name__)
app.secret_key = os.urandom(64)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=30)

RECAPTCHA_SECRET_KEY = 'TU_CLAVE_SECRETA'

# Ruta para el inicio
@app.route("/")
def h():
    return redirect("/inicio")

# Ruta para el inicio
@app.route("/inicio")
def home():
    return render_template("home.html")

# Ruta para el blog
@app.route("/blog")
def blog():
    i = imprimir()
    return render_template("blog.html", data=i)

# Ruta para el administrador
@app.route("/admin")
def admin():
    if "id" in session and session.get("rol") == "admin":
        noticias = imprimir()
        return render_template("admin.html", noticias=noticias)
    else:
        return redirect("/login")

# Ruta para el inicio de sesión
@app.route("/login")
def login():
    return render_template("login.html")




# Ruta para la validación del inicio de sesión
@app.route("/validacion_login", methods=["POST"])
def validacion_login():
    email = request.form.get("email")
    password = request.form.get("password")


      # Inicializar el contador de intentos de sesión si no existe
    if 'login_attempts' not in session:
        session['login_attempts'] = 0

    # Verificar si se han excedido los intentos de sesión
    if session['login_attempts'] >= 3:
        return "Has excedido el número de intentos de inicio de sesión. Intenta más tarde."

    es_valido, datos = verificar_password(email, password)
# Verificar si la autenticación es exitosa
    if es_valido:  # Si la autenticación es exitosa
        session["id"] = datos.id
        session["rol"] = datos.rol
        session['login_attempts'] = 0  # Reiniciar el contador de intentos de sesión
        if datos.rol == "admin":
            return redirect("/admin")

        else:
            return redirect("/inicio")
    else:
        session['login_attempts'] += 1  # Incrementar el contador de intentos de sesión
        return redirect("/login")



# Ruta para el registro de usuarios

@app.route("/registro")
def registro():
    return render_template("registro.html")

# Ruta para la validación del registro de usuarios
@app.route("/validacion_registro", methods=["POST"])
def validacion_registro():
    unombre = request.form.get("unombre")
    uemail = request.form.get("uemail")
    upassword = request.form.get("upassword")

    nuevo_usuario  = Usuario(nombre=unombre,email=uemail,password=generar_hass(upassword))
    crear_usuario(nuevo_usuario)
    return redirect("/login")

    

# Ruta para cerrar sesión
@app.route("/cerrar_sesion")
def cerrar_sesion():
    session.clear()
    return redirect("/inicio")



"""" blog comprimir imagenes """


UPLOAD_FOLDER = "static/img"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ruta para subir archivos
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No file part"
    file = request.files["file"]
    if file.filename == "":
        return "No selected file"
    if file and file.filename.endswith((".jpg", ".jpeg", ".png")):
        filename = file.filename
        direccion = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(direccion)
        tamano_img(direccion)
        # tamaño de la imagen
        registrar(
            request.form.get("titulo"), request.form.get("descripcion"), direccion
        )
        #print("la direccio es : -----------------   " + direccion)
        mensaje= "El archivo se ha subido correctamente"
        return render_template("admin.html",  mensaje=mensaje)
# Ruta para borrar una noticia
@app.route("/borrar/<int:noticia_id>")
def borrar(noticia_id):
    if "id" in session and session.get("rol") == "admin":
        if borrar_noticia(noticia_id):
            return redirect("/admin")
        else:
            return "Error al borrar la noticia", 404
    else:
        return redirect("/login")






if __name__ == "__main__":
    app.run(debug=True)
