"""
main.py es el modulo principal donde se encuentra el controlador de la applicacion.\n
Este modulo contiene :
    :Clase Controller: Crea el objeto VistaApp asignandolo al atributo objeto_vista.
    :Inicializacion de la ventana principal: Se crea la intancia de la clase Tk y el bucle principal.
    :Objeto de la clase Controller: Se crea el objeto de la clase y se lo asignandolo al atributo aplicacion
    :Metodo actualizar:  Se llama al metodo actualizar del objeto objeto_vista,
                         la cual actualiza el treeview al iniciar la applicacion. 
"""

__author__ = "Samuel Montenegro"
__maintainer__ = "Samuel Montenegro"
__email__ = "montenegroasm555@gmail.com"
__copyright__ = "Copyright 2024"
__version__ = "0.1"


# -*- coding: utf-8 -*-
# Se importa la clase Tk para crear la ventana principal.
from tkinter import Tk

# Se importa el modulo Vista.
import vista


# Clase principal
class Controller:
    """
    Clase principal del modulo main.py
    """

    def __init__(self, root):
        """
        Esta clase crea al objeto VistaApp asignandolo al atributo objeto_vista.
        """
        self.root = root
        # Se crea el objeto VistaApp y se lo asigna a objetivo_vista
        self.objeto_vista = vista.VistaApp(self.root)


# Condición que verifica si el script se está ejecutando como el programa principal.
if __name__ == "__main__":
    """
    Crea una instancia de la clase Tk, que representa la ventana principal de la aplicación.
    Tambien inicia el bucle principal.

    """
    root = Tk()
    aplicacion = Controller(root)
    aplicacion.objeto_vista.actualizar()
    # Inicia el bucle principal
    root.mainloop()
