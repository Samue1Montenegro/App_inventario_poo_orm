"""
base_datos.py es el modulo donde se encuentran :\n
  - El modelo de datos utilizando el ORM Pewee, conectado con Sqlite.
  - Definicion de ruta/directorio en la que el archivo "mi_base.db" aparecera.
  - Creacion de la tabla de la base de datos y definicion de campos que representen las columnas.
  - Se establece la conexion de la base de datos.
  - Manejo de posibles errores que podrian ocurrir. 

"""

# -*- coding: utf-8 -*-
# Se importa el modulo OS para interactuar con el sistema operativo
import os

# Se importan las librerias de pewee para conectar con Sqlite
from peewee import *


try:
    # Obtiene la ruta absoluta del directorio en el que se encuentra el script
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Define la ruta de la base de datos relativa al directorio del script
    database_filename = "mi_base.db"
    database_path = os.path.join(script_directory, database_filename)

    # Crea un objeto "db" instanciando SqliteDatabase con la ruta relativa al directorio del script
    db = SqliteDatabase(database_path)
    print("Ruta de la base de datos:", db.database)

    class Table(Model):
        """
        Aquí se define una clase llamada Table que hereda de la clase Model
        Model es una clase base proporcionada por peewee para definir modelos de bases de datos.
        """

        # Se definen tres campos de la tabla,
        # que representarán las columnas en la tabla de la base de datos.
        codigo = IntegerField(unique=True)
        producto = CharField()
        cantidad = IntegerField()

        class Meta:
            """
            La clase Meta se utiliza para proporcionar metadatos sobre el modelo
            """

            # Indicamos a peewee que esta tabla está asociada con la base de datos db
            database = db

    # Se establece una conexión y se crea las tabla con la base de datos
    db.connect()
    db.create_tables([Table])

# Se manejan excepciones para diferentes tipos de errores
except FileNotFoundError as a:
    print(f"Error: No se encontró el archivo: {a}")
except Exception as e:
    print(f"Error inesperado: {e}")
else:
    print("¡Base de datos creada exitosamente!")
finally:
    # Cierra la conexión con la base de datos, independientemente de si hubo errores o no
    db.close()
