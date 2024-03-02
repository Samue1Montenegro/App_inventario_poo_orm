"""
vista.py es el modulo encargado de contener toda la configuracion de la interfaz grafica.\n
En este modulo se encuentra la clase principal VistaApp la cual contiene:
    :Iniciacion de la ventana de la app: Su configuracion predeterminada, titulos, formularios.
    :Treeview: Columnas, filas, barra de desplazamiento
    :Botones: Botones para agregar, borrar, modificar producto, consulta,
     actualizar, tema

En el modulo tambien se encuentran funciones para invocar a los metodos del modulo modelo.py:
    :Alta: llama a al metodo alta, contiene excepciones para manejo de errores y notificaciones.
    :Borrar: llama a al metodo borrar, contiene excepciones para manejo de errores y notificaciones.
    :Modificar: llama a al metodo modificar_seleccionado, contiene excepciones para manejo de errores y notificaciones.
    :Consulta: llama a al metodo realizar_consulta, contiene excepciones para manejo de errores y notificaciones.
    :Actualizar: llama a al metodo actualizar_treeview, contiene excepciones para manejo de errores y notificaciones.

"""

# -*- coding: utf-8 -*-
# Se importa ttk para crear widgets.
from tkinter import ttk

# Asigna el modulo tkinter a tk para facilitar su uso.
import tkinter as tk

# Se importa la clase Label para mostrar texto o imágenes en una ventana de la interfaz.
from tkinter import Label

# Se importa la clase Entry para crear campos de entrada de texto.
from tkinter import Entry

# Se importa la clase Scrollbar para agregar barra de desplazamiento en el Treeview.
from tkinter import Scrollbar

# Se importa la clase Button para crear botones en una interfaz.
from tkinter import Button

import webview

# Se importa desde el modulo notificaciones la clase Notificacion
from notificaciones import Notificacion

# Se crea el objeto notificar instanciando la clase importada
notificar = Notificacion

# Se impora desde el modulo documentacion_html la clase ServicioHtml
from documentacion_html import DocumentHtml

# Se importan funciones desde el modulo modelo para ser utilizadas.

from modelo import Abmc

from temas import Tema


# ----------------------------------------------------------------------------------
# ######################       VISTA                ########################
# ----------------------------------------------------------------------------------


# clase que contiene la estructura y vista de la interfaz
class VistaApp:
    """Clase principal del modulo 'vista.py'"""

    def __init__(self, root):
        self.root = root
        """Ventana principal"""
        self.tree = ttk.Treeview(
            self.root, columns=("ID", "Producto", "Cantidad"), show="headings"
        )

        # Se crea un titulo para la ventana.
        self.root.title("Inventario")
        self.root.configure(bg="#F2F3F4")
        self.abmc_import = Abmc(self.tree)
        self.tema = Tema(self.root)
        self.archivo = DocumentHtml(self.root)
        # Titulo general de la aplicacion.
        self.titulo = Label(
            self.root,
            text="INGRESE SUS PRODUCTOS",
            bg="#00758f",
            fg="white",
            height=3,
            width=60,
        )
        self.titulo.grid(
            row=0, column=0, columnspan=4, padx=1, pady=1, sticky="w" + "e"
        )

        # Titulos que indican en la entrada de datos en productos y configuracion de posicion.
        self.producto = Label(self.root, text="PRODUCTO")
        self.producto.grid(row=1, column=0, sticky="w")

        # Titulos que indican en la entrada de datos en cantidad y configuracion de posicion.
        self.cantidad = Label(self.root, text="CANTIDAD")
        self.cantidad.grid(row=2, column=0, sticky="w")

        # Titulos que indican en la entrada de datos en codigo del producto y configuracion de posicion.
        self.id_prod = Label(self.root, text="CODIGO")
        self.id_prod.grid(row=3, column=0, sticky="w")

        # Titulos que indican en la entrada de datos en consulta y configuracion de posicion.
        self.consulta_label = Label(self.root, text="CONSULTA DEL PRODUCTO")
        self.consulta_label.grid(row=4, column=0, sticky="w")
        self.w_ancho = 40

        # Se definen variables para tomar valores de campos de entrada.
        self.producto_val = tk.StringVar()
        self.consulta_val = tk.StringVar()
        self.cantidad_val = tk.IntVar()
        self.codigo_val = tk.IntVar()

        # Formulario para Campo de entrada de producto.
        self.entrada_producto = Entry(
            self.root, textvariable=self.producto_val, width=self.w_ancho
        )
        self.entrada_producto.grid(row=1, column=1)
        self.entrada_producto.focus()

        # Formulario para Campo de entrada en cantidad del producto.
        self.entrada_cantidad = Entry(
            self.root, textvariable=self.cantidad_val, width=self.w_ancho
        )
        self.entrada_cantidad.grid(row=2, column=1)

        # Formularios para Campo de entrada del codigo del producto.
        self.entrada_codigo = Entry(
            self.root, textvariable=self.codigo_val, width=self.w_ancho
        )
        self.entrada_codigo.grid(row=3, column=1)

        # Formulario para Campo de consulta de producto
        self.consulta_entry = Entry(
            self.root,
            textvariable=self.consulta_val,
            width=self.w_ancho,
        )
        self.consulta_entry.grid(row=4, column=1)

        # ----------------------------------------------------------------------------------
        # ######################          TREEVIEW             ######################
        # ----------------------------------------------------------------------------------

        # Columnas para Producto, codigo y cantidad
        self.tree["columns"] = ("ID", "Producto", "Cantidad")
        self.tree.column("ID", width=100, minwidth=50, anchor="center")
        self.tree.column("Producto", width=300, minwidth=80, anchor="center")
        self.tree.column("Cantidad", width=300, minwidth=80, anchor="center")

        # Nombre de columnas
        self.tree.heading("ID", text="CODIGO")
        self.tree.heading("Producto", text="PRODUCTO")
        self.tree.heading("Cantidad", text="CANTIDAD")
        self.tree.grid(row=10, column=0, columnspan=4)

        # Crear un estilo para el Treeview y se le asigna un color de fondo por defecto
        style = ttk.Style()
        style.configure("Treeview", background="#00758f")

        # Aplicar el estilo al Treeview
        self.tree.tag_configure("Treeview", background="#00758f")

        # Crea la barra de deslizamiento vertical.
        self.tree_scrollbar = Scrollbar(self.root, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.tree_scrollbar.set)
        self.tree_scrollbar.grid(row=10, column=4, sticky="ns")

        # Crea una barra de separacion
        self.separador = ttk.Separator(
            self.root,
            orient="horizontal",
        )
        self.separador.grid(row=6, pady=4)

        """Boton para dar de alta un producto y sus configuraciones."""
        self.boton_alta = Button(
            self.root,
            text="Agregar",
            width=10,
            activeforeground="green",
            cursor=("hand2"),
            command=lambda: self.alta(),
        )
        self.boton_alta.grid(row=1, column=2)

        """Boton para borrar un producto y sus configuraciones."""
        self.boton_borrar = Button(
            self.root,
            text="Borrar",
            width=10,
            activeforeground="red",
            cursor=("hand2"),
            command=lambda: self.borrar(),
        )
        self.boton_borrar.grid(row=2, column=2, pady=(1, 0))

        """Se crea el botón Modificar Producto para modificar el elemento seleccionado y las configuraciones del boton."""
        self.modificar_boton = Button(
            self.root,
            text="Modificar Producto",
            activeforeground="cyan",
            cursor=("hand2"),
            command=lambda: self.modificar(),
        )
        self.modificar_boton.grid(row=3, column=2, pady=(1, 0))

        """Boton para realizar una consulta sobre un producto y sus configuraciones."""
        self.boton_consulta = Button(
            self.root,
            text="Consultar",
            width=10,
            activeforeground="yellow",
            cursor=("hand2"),
            command=lambda: self.consulta(),
        )
        self.boton_consulta.grid(row=4, column=2, pady=(1, 0))

        """Boton para poder actualizar el inventario luego de realizar una consulta y sus configuraciones."""
        self.boton_actualizar = Button(
            self.root,
            text="Actualizar",
            width=10,
            activeforeground="deep pink",
            cursor=("hand2"),
            command=lambda: self.actualizar(),
        )
        self.boton_actualizar.grid(row=5, column=2, pady=(1, 0))

        """Botón para cambiar el tema de fondo"""
        self.boton_tema = Button(
            self.root,
            variable=self.root.configure(bg="#F2F3F4"),
            text="Temas",
            activebackground="green2",
            cursor=("hand2"),
            command=lambda: self.tema.cambiar_tema(),
        )
        self.boton_tema.grid(row=1, column=3, pady=(1, 0))

        """Boton para abrir la documentacion de la app"""
        self.boton_doc = tk.Button(
            self.root,
            text="Documentacion",
            activeforeground="red",
            command=self.abrir_archivo_html,
        )
        self.boton_doc.grid(row=5, column=3, pady=(1, 0))

    # Se crea una funcion para instanciar al metodo alta de la clase abmc
    # y poder utilizarlo en el boton alta
    def alta(
        self,
    ):
        """Este metodo llama al metodo 'alta' ubicado en el modulo modelo
        y se llama desde el boton consulta.\n
        Si el producto se crea exitosamente se le notifica al usuario en pantalla.\n
        En caso de ocurrir un error se le notifica al usuario en pantalla."""
        try:

            if (
                self.abmc_import.alta(
                    self.codigo_val,
                    self.producto_val,
                    self.cantidad_val,
                )
                is True
            ):
                # Se notifica al usuario de la acción exitosa.
                notificar.mostrar_notificacion("Producto agregado con éxito.")
            else:
                # Se notifica al usuario de un error en campos de entrada
                notificar.mostrar_notificacion(
                    "Elementos no válidos.!\n Para Producto: Solo letras incluida la ñ, números, caracteres /, _, ' y espacios permitidos.\n"
                    "Para Cantidad: Solo números enteros y decimales separados con una coma.\n"
                    "Para número ID/Código: Solo números enteros."
                )
        except:
            # Se notifica al usuario de un error en campos de entrada
            notificar.mostrar_notificacion(
                "Elementos no válidos.!\n Para Producto: Solo letras incluida la ñ, números, caracteres /, _, ' y espacios permitidos.\n"
                "Para Cantidad: Solo números enteros y decimales separados con una coma.\n"
                "Para número ID/Código: Solo números enteros."
            )

    # Se crea una funcion para instanciar al metodo borrar de la clase abmc
    # y poder utilizarlo en el boton borrar
    def borrar(
        self,
    ):
        """Este metodo llama al metodo 'borrar' ubicado en el modulo modelo
        y se llama desde el boton consulta.\n
        Si el producto se borra exitosamente, se notifica al usuario en pantalla.\n
        En caso de ocurrir un error se le notifica al usuario en pantalla."""
        try:
            self.abmc_import.borrar()
        except Exception as b:
            notificar.mostrar_notificacion(
                f"Ocurrió un error al eliminar el elemento.\n{str(b)}"
            )
        else:
            # Se le notifica al usuario que la acción es exitosa.
            notificar.mostrar_notificacion("Elemento eliminado con éxito.")

    # Se crea una funcion para instanciar al metodo modificar_seleccionado de la clase abmc
    # y poder utilizarlo en el boton modificar
    def modificar(
        self,
    ):
        """Este metodo llama al metodo 'modificar_seleccionado' ubicado en el modulo modelo
        y se llama desde el boton consulta.\n
        Si se modifica el producto exitosamente, se notifica al usuario en pantalla\n
        En caso de ocurrir un error se le notifica al usuario en pantalla."""
        try:
            self.abmc_import.modificar_seleccionado()
        except Exception as c:
            notificar.mostrar_notificacion(
                f"Error en la seleccion de producto.\n{str(c)}"
            )
        else:
            notificar.mostrar_notificacion("Producto modificado con éxito!")

    # Se crea una funcion para instanciar al metodo realizar_consulta de la clase abmc
    # y poder utilizarlo en el boton alta
    def consulta(
        self,
    ):
        """Este metodo llama al metodo 'realizar_consulta' ubicado en el modulo modelo
        y se llama desde el boton consulta.\n
        En caso de ocurrir un error se le notifica al usuario en pantalla."""
        try:
            self.abmc_import.realizar_consulta(self.consulta_val)
        except Exception as d:
            # Se le notifica al usuario en caso de error y se muestran detalles del error.
            notificar.mostrar_notificacion(
                f"Hubo un error al realizar la consulta\n: {str(d)}"
            )

    # Se crea una funcion para instanciar al metodo actualizar_treeview de la clase abmc
    # y poder utilizarlo en el boton alta
    def actualizar(
        self,
    ):
        """Este metodo llama al metodo 'actualizar_treeview' ubicado en el modulo modelo
        y se llama desde el boton actualizar.\n
        En caso de ocurrir un error se le notifica al usuario en pantalla."""
        try:
            self.abmc_import.actualizar_treeview(self.tree)
        except Exception as e:
            # Se le notifica al usuario en caso de error y se muestran detalles del error.
            notificar.mostrar_notificacion(
                f"Hubo un error al actualizar el treeview\n: {str(e)}"
            )

    # Metodo para crear e iniciar la ventana html
    def mostrar_html(self, archivo_html):
        """
        Metodo que muestra la ventana con el archivo html deseado:
        Args:
          - archivo_html: ruta del archivo html, definido en documentacion_html
        Type:
          - archivo_html: str
         - Utiliza la función 'create_window' de la biblioteca 'webview',
           para crear una nueva ventana con un visor 'HTML'.
         - Se inicia el bucle principal de eventos de 'webview'.
        """
        webview.create_window("Visor HTML", url=f"file://{archivo_html}")
        webview.start()

    def abrir_archivo_html(self):
        """Este metodo obtiene la ruta del archivo html, utilizando esta ruta
        para mostrar el contenido en la ventana que crea 'mostrar_html'
        Se llamara este metodo desde el boton 'boton_doc'"""
        archivo_html = self.archivo.obtener_archivo_html()
        self.mostrar_html(archivo_html)
