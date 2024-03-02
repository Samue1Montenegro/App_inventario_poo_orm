"""
temas.py es el modulo el cual contiene la logica para cambiar el tema de fondo de la aplicacion.\n
Este modulo contiene la clase principal del modulo Tema en el que se encuentran los siguientes metodos:
    :El metodo cambiar_tema: Configura el tema para que su color de fondo sea aleatoreo.

"""

# -*- coding: utf-8 -*-
# Se importa el módulo random para generar numeros aleatoreos
import random


# Definición de la clase Tema
class Tema:
    """Clase principal del modulo temas"""

    def __init__(self, root):
        self.root = root

    # Método para cambiar el tema de la aplicación
    def cambiar_tema(
        self,
    ):
        """
        Este metodo se destina a el cambio de tema de la aplicacion:
         - Se genera un color aleatorio
         - Se configura el color de fondo
        :return: none
        """
        # Genera un color aleatorio
        color_nuevo = "#{:02x}{:02x}{:02x}".format(
            random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        )
        # Configura el color de fondo
        self.root.configure(bg=color_nuevo)
