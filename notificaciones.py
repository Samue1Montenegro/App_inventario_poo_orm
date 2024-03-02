"""
notificaciones.py es el modulo encargado realizar las notificaciones para mostrarlas en pantalla.\n
Este modulo contiene :
   :La clase Notificacion: Clase principal del modulo.
   :El metodo mostrar_notificacion: Metodo que contiene la logica.

"""

# -*- coding: utf-8 -*-
# Importa messagebox para poder realizar notificaciones como mensajes de alerta o confirmaciones
from tkinter import messagebox


class Notificacion:
    """Clase principal del modulo notificaciones"""

    # Metodo para poder mostrar notificaciones en las acciones o mostrar errores.
    def mostrar_notificacion(mensaje):
        """
        Este metodo incorpora funcion messagebox del modulo tkinter
        para poder mostrar notificaciones en pantalla.
         Args:
            - mensaje: Incorpora el mesaje deseado segun la notificacion
         Type:
            - mensaje: str
        """
        messagebox.showinfo("Notificación", mensaje)
