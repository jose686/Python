from PIL import Image


def tamano_img(file):
        imagen = Image.open(file)
        imagen_redimensionada = imagen.resize((1280, 720))
        imagen_redimensionada.save(file, "JPEG",  quality=80, optimize=True)
        print("Imagen redimensionada")
        
