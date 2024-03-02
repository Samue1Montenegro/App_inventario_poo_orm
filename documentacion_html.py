"""
documentacion_html.py es el modulo el cual tiene como logica calcular 
la ruta de directorio el cual se encuentra el archivo Html
de la documentacion de la app

"""

# -*- coding: utf-8 -*-
# Se importa el modulo OS para interactuar con el sistema operativo
import os


class DocumentHtml:
    """
    Clase DocumentHtml para manejar operaciones relacionadas con archivos HTML.

    Esta clase ofrece funcionalidades para interactuar con archivos HTML,
    como obtener la ruta de un archivo HTML específico (Documentacion de la app).
    """

    def __init__(self, root):
        self.root = root

    def obtener_archivo_html(self):
        """
        Obtiene la ruta del archivo HTML deseado.

        Calcula y retorna la ruta del archivo HTML basada en la ubicación actual
        del script. Se asume que el archivo HTML está ubicado en un subdirectorio
        'docs/_build/html' relativo al directorio donde se encuentra este script.

        Returns:
            str: La ruta del archivo HTML.
        """
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        archivo_html = os.path.join(
            directorio_actual, "docs", "_build", "html", "index.html"
        )
        return archivo_html
