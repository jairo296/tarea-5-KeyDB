
import json
from database import keydb


# GENERAR IDENTIFICADOR

def siguiente_id():
    return keydb.incr("libros:ultimo_id")


# VALIDAR DATOS

def validar_datos(titulo, autor, genero, estado):

    if not titulo or not titulo.strip():
        return False, "El título es obligatorio."

    if not autor or not autor.strip():
        return False, "El autor es obligatorio."

    if not genero or not genero.strip():
        return False, "El género es obligatorio."

    if estado not in ["Pendiente", "Leyendo", "Terminado"]:
        return False, "El estado de lectura no es válido."

    return True, "Datos válidos."


# OBTENER LIBROS

def obtener_libros():

    libros = []

    for clave in keydb.scan_iter(match="libro:*"):

        datos = keydb.get(clave)

        if datos:

            libro = json.loads(datos)

            # Compatibilidad con libros anteriores
            libro.setdefault("portada", None)

            libros.append(libro)

    return sorted(libros, key=lambda libro: libro["id"])


# COMPROBAR SI EXISTE UN LIBRO

def existe_libro(titulo, autor, excluir_id=None):

    for libro in obtener_libros():

        if libro["id"] == excluir_id:
            continue

        mismo_titulo = (
            libro["titulo"].casefold() == titulo.strip().casefold()
        )

        mismo_autor = (
            libro["autor"].casefold() == autor.strip().casefold()
        )

        if mismo_titulo and mismo_autor:
            return True

    return False


# AGREGAR LIBRO

def agregar_libro(titulo, autor, genero, estado, portada=None):

    valido, mensaje = validar_datos(
        titulo, autor, genero, estado
    )

    if not valido:
        return False, mensaje

    try:

        if existe_libro(titulo, autor):
            return False, "Este libro ya está registrado."

        nuevo_libro = {
            "id": siguiente_id(),
            "titulo": titulo.strip(),
            "autor": autor.strip(),
            "genero": genero.strip(),
            "estado": estado,
            "portada": portada
        }

        keydb.set(
            f"libro:{nuevo_libro['id']}",
            json.dumps(nuevo_libro, ensure_ascii=False)
        )

        return True, "Libro agregado correctamente."

    except Exception as error:
        return False, f"Error al agregar el libro: {error}"


# MOSTRAR LIBROS

def mostrar_libros():

    try:
        return obtener_libros()

    except Exception as error:
        print(f"Error al mostrar los libros: {error}")
        return []


# BUSCAR LIBROS

def buscar_libros(texto):

    try:

        resultados = obtener_libros()
        texto = texto.strip().casefold()

        if not texto:
            return resultados

        encontrados = [
            libro for libro in resultados
            if any(
                texto in str(libro.get(campo, "")).casefold()
                for campo in ("titulo", "autor", "genero")
            )
        ]

        return encontrados

    except Exception as error:
        print(f"Error al buscar libros: {error}")
        return []


# ACTUALIZAR LIBRO

def actualizar_libro(
    id_libro,
    titulo,
    autor,
    genero,
    estado,
    portada=None
):

    valido, mensaje = validar_datos(
        titulo, autor, genero, estado
    )

    if not valido:
        return False, mensaje

    try:

        clave = f"libro:{id_libro}"
        datos = keydb.get(clave)

        if datos is None:
            return False, "No se encontró el libro."

        if existe_libro(titulo, autor, excluir_id=id_libro):
            return False, "Ya existe otro libro con ese título y autor."

        libro = json.loads(datos)

        libro.update({
            "titulo": titulo.strip(),
            "autor": autor.strip(),
            "genero": genero.strip(),
            "estado": estado
        })

        # Cambiar portada solamente si se proporciona una nueva
        if portada:
            libro["portada"] = portada

        else:
            libro.setdefault("portada", None)

        keydb.set(
            clave,
            json.dumps(libro, ensure_ascii=False)
        )

        return True, "Libro actualizado correctamente."

    except Exception as error:
        return False, f"Error al actualizar el libro: {error}"


# ELIMINAR LIBRO

def eliminar_libro(id_libro):

    try:

        eliminado = keydb.delete(f"libro:{id_libro}")

        if eliminado == 0:
            return False, "No se encontró el libro."

        return True, "Libro eliminado correctamente."

    except Exception as error:
        return False, f"Error al eliminar el libro: {error}"
