# Biblioteca Personal con KeyDB

## Descripción

Biblioteca Personal es una aplicación web desarrollada en Python utilizando Flask y KeyDB. Permite administrar una colección personal de libros mediante una interfaz gráfica sencilla e intuitiva.

Los registros se almacenan en KeyDB en formato JSON, mientras que las imágenes de portada se guardan localmente en el servidor.

## Funcionalidades

- Registrar libros.
- Visualizar la colección.
- Buscar por título, autor o género.
- Editar información de los libros.
- Eliminar libros.
- Asignar y cambiar imágenes de portada.
- Seleccionar el estado de lectura.
- Validar campos obligatorios.
- Evitar registros duplicados por título y autor.

## Tecnologías utilizadas

- Python
- Flask
- KeyDB
- Redis-py
- HTML5
- CSS3
- Jinja2
- JSON
- Docker
- python-dotenv

## Requisitos previos

- Python 3 instalado.
- Docker Desktop instalado y ejecutándose.
- KeyDB disponible mediante Docker.

## Instalación y ejecución

### 1. Iniciar KeyDB

Para crear el contenedor por primera vez:

    docker run -d --name biblioteca-keydb-server -p 6379:6379 eqalpha/keydb

Si el contenedor ya existe:

    docker start biblioteca-keydb-server

### 2. Instalar dependencias

Desde la carpeta principal del proyecto:

    python -m pip install -r requirements.txt

### 3. Configurar las variables de entorno

Crear el archivo `.env` copiando la plantilla:

    Copy-Item .env.example .env

Abrir el archivo `.env` y configurar una clave secreta propia en `SECRET_KEY`.

Variables necesarias:

    KEYDB_HOST=localhost
    KEYDB_PORT=6379
    KEYDB_PASSWORD=
    KEYDB_DB=0
    SECRET_KEY=colocar_una_clave_secreta

No compartir el archivo `.env`, ya que contiene información privada.

### 4. Ejecutar la aplicación

    python app.py

Abrir el navegador en:

http://127.0.0.1:5000

## Almacenamiento de datos

Los libros se almacenan en KeyDB mediante claves con el formato:

`libro:<id>`

La información de cada libro se serializa en formato JSON.

El contador de identificadores se almacena en:

`libros:ultimo_id`

Las imágenes de portada se guardan en:

`static/uploads/`

## Estructura del proyecto

    Entrega_Biblioteca_KeyDB/
    |
    |-- app.py
    |-- config.py
    |-- database.py
    |-- crud.py
    |-- requirements.txt
    |-- README.md
    |-- .gitignore
    |-- .env.example
    |
    |-- static/
    |   |-- style.css
    |   |-- uploads/
    |
    |-- templates/
        |-- base.html
        |-- index.html
        |-- agregar.html
        |-- editar.html

## Autor

Proyecto académico desarrollado para la asignatura de Programación de Computadoras IV.
