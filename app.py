
import os
import uuid

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from werkzeug.utils import secure_filename

from config import Config
from database import keydb

from crud import (
    agregar_libro,
    mostrar_libros,
    buscar_libros,
    actualizar_libro,
    eliminar_libro
)


# CONFIGURACION DE FLASK

app = Flask(__name__)
app.config.from_object(Config)

CARPETA_UPLOADS = os.path.join(
    app.root_path,
    "static",
    "uploads"
)

EXTENSIONES_PERMITIDAS = {
    "jpg",
    "jpeg",
    "png",
    "webp"
}

os.makedirs(CARPETA_UPLOADS, exist_ok=True)


# VALIDAR EXTENSION DE IMAGEN

def archivo_permitido(nombre):

    return (
        "." in nombre
        and nombre.rsplit(".", 1)[1].lower()
        in EXTENSIONES_PERMITIDAS
    )


# GUARDAR IMAGEN

def guardar_portada(archivo):

    if not archivo or not archivo.filename:
        return None

    if not archivo_permitido(archivo.filename):
        raise ValueError("Formato de imagen no permitido.")

    nombre_seguro = secure_filename(archivo.filename)

    extension = nombre_seguro.rsplit(".", 1)[1].lower()

    nombre_final = f"{uuid.uuid4().hex}.{extension}"

    ruta = os.path.join(
        CARPETA_UPLOADS,
        nombre_final
    )

    archivo.save(ruta)

    return nombre_final


# ELIMINAR IMAGEN

def borrar_portada(nombre):

    if not nombre:
        return

    nombre_seguro = os.path.basename(nombre)

    ruta = os.path.join(
        CARPETA_UPLOADS,
        nombre_seguro
    )

    if os.path.isfile(ruta):
        os.remove(ruta)


# PAGINA PRINCIPAL Y BUSQUEDA

@app.route("/")
def index():

    texto = request.args.get("buscar", "").strip()

    if texto:
        libros = buscar_libros(texto)
    else:
        libros = mostrar_libros()

    return render_template(
        "index.html",
        libros=libros
    )


# AGREGAR LIBRO

@app.route("/agregar", methods=["GET", "POST"])
def agregar():

    if request.method == "POST":

        titulo = request.form.get("titulo", "")
        autor = request.form.get("autor", "")
        genero = request.form.get("genero", "")
        estado = request.form.get("estado", "")

        archivo = request.files.get("portada")
        portada = None

        try:

            if archivo and archivo.filename:
                portada = guardar_portada(archivo)

            exito, mensaje = agregar_libro(
                titulo,
                autor,
                genero,
                estado,
                portada
            )

            if exito:
                flash(mensaje, "success")
                return redirect(url_for("index"))

            if portada:
                borrar_portada(portada)

            flash(mensaje, "error")

        except Exception as error:

            if portada:
                borrar_portada(portada)

            flash(
                f"Error al registrar el libro: {error}",
                "error"
            )

    return render_template("agregar.html")


# EDITAR LIBRO

@app.route("/editar/<int:id_libro>", methods=["GET", "POST"])
def editar(id_libro):

    libros = mostrar_libros()

    libro = next(
        (l for l in libros if l["id"] == id_libro),
        None
    )

    if libro is None:
        flash("No se encontró el libro solicitado.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":

        titulo = request.form.get("titulo", "")
        autor = request.form.get("autor", "")
        genero = request.form.get("genero", "")
        estado = request.form.get("estado", "")

        archivo = request.files.get("portada")
        nueva_portada = None

        try:

            if archivo and archivo.filename:
                nueva_portada = guardar_portada(archivo)

            exito, mensaje = actualizar_libro(
                id_libro,
                titulo,
                autor,
                genero,
                estado,
                nueva_portada
            )

            if exito:

                if nueva_portada and libro.get("portada"):
                    borrar_portada(libro["portada"])

                flash(mensaje, "success")
                return redirect(url_for("index"))

            if nueva_portada:
                borrar_portada(nueva_portada)

            flash(mensaje, "error")

        except Exception as error:

            if nueva_portada:
                borrar_portada(nueva_portada)

            flash(
                f"Error al actualizar el libro: {error}",
                "error"
            )

    return render_template(
        "editar.html",
        libro=libro
    )


# ELIMINAR LIBRO

@app.route("/eliminar/<int:id_libro>", methods=["POST"])
def eliminar(id_libro):

    libros = mostrar_libros()

    libro = next(
        (l for l in libros if l["id"] == id_libro),
        None
    )

    try:

        exito, mensaje = eliminar_libro(id_libro)

        if exito:

            if libro:
                borrar_portada(libro.get("portada"))

            flash(mensaje, "success")

        else:
            flash(mensaje, "error")

    except Exception as error:

        flash(
            f"Error al eliminar el libro: {error}",
            "error"
        )

    return redirect(url_for("index"))


# EJECUTAR APLICACION

if __name__ == "__main__":

    try:

        keydb.ping()

        print("Conexion con KeyDB exitosa.")
        print("Iniciando Biblioteca Personal...")

        app.run(
            host="127.0.0.1",
            port=5000,
            debug=app.config["DEBUG"]
        )

    except Exception as error:

        print(f"Error al conectar con KeyDB: {error}")
        print("Verifica que el contenedor de KeyDB este funcionando.")
