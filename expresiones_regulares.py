"""
expresiones_regulares.py es el modulo el cual se encarga de verificar los campos de entrada.\n
La clase principal del modulo es ReguCampos el cual contiene :
   - El metodo expresion_alta: Contiene la logica para verificar los campos de entrada especificos a cada uno.

"""

# -*- coding: utf-8 -*-
# Importamos el modulo re para establecer expresiones regulares
import re


class ReguCampos:
    """
    Clase principal del modulo expresiones_regulares
    """

    def expresion_alta(valor_codigo, valor_producto, valor_cantidad):
        """
        Este metodo contiene:
         Args:
           - valor_codigo: El codigo del producto.
         Type:
            -  valor_codigo: int
         Args:
            - valor_producto: El nombre del producto.
         Type:
            - valor_producto: str
         Args:
            - valor_cantidad: La cantidad del producto.
         Type:
            - valor_cantidad: int
         - Expresiones regulares para controlar los campos de entrada.
         - Se verifica que los campos coincidan con las expresiones definidas.
        Returns:
         - True: Si los campos son correctos.
         - False: Si los campos son incorrectos.
        """
        patron_id_prod = "^[0-9]+$"
        patron_producto = "^[A-Za-záéíóúñÑ0-9\s/_']+$"
        patron_cantidad = "^[0-9]+$"
        # Se verifica que los campos coincidan con las expresiones definidas
        # Retorna True si los campos son correctos y False si uno o todos son incorrectos
        return (
            re.fullmatch(patron_id_prod, valor_codigo)
            and re.fullmatch(patron_producto, valor_producto)
            and re.fullmatch(patron_cantidad, valor_cantidad)
        )
