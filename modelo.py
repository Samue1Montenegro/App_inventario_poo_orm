"""
modelo.py es el modulo en el que se establecen las principales funcionalidades de la aplicacion.\n
Al ser una aplicacion CRUD este modulo contiene una clase principal llamada Abmc.\n
La Clase Abmc contiene :
   :El metodo alta: Agrega productos nuevos
   :El metodo borrar: Borra productos existentes
   :El metodo modificar_seleccionado: Modifica un producto seleccionado del Treeview
   :El metodo realizar_consulta: Realiza una consulta mediante una palabra clave
   :El metodo actualizar_treeview: Actualiza el treeview luego de cualquier operacion,
        tambien se actualiza manualmente

"""

# -*- coding: utf-8 -*-
# Importa simpledialog para poder lanzar un cuadro de dialogo simple, en este caso para poder modificar datos mediante un campo de entrada.
from tkinter import simpledialog

# Importa la excepción específica de Peewee para la integridad de la base de datos
from peewee import IntegrityError

# Se importa la clase Table del modulo BaseDatos
from base_datos import Table

# Se importa la clase Regucampos del modulo ExpresionesRegulares
from expresiones_regulares import ReguCampos

# Se importa la clase Notificacion del modulo notificaciones
from notificaciones import Notificacion

# Se crea objetos instanciando a las clases para utilizarlas
validacion_alta = ReguCampos
notificar = Notificacion

# ----------------------------------------------------------------------------------
# ######################      MODELO              ########################
# ----------------------------------------------------------------------------------


class Abmc:
    """
    Clase principal del modulo 'modulo.py'\n
     :Abmc hace referencia al sistema 'CRUD':
     - Alta
     - Borrar
     - Modificacion
     - Consulta"""

    def __init__(self, tree):
        self.tree = tree

    def alta(self, codigo, producto, cantidad):
        """
        Metodo principal del 'CRUD' en el que se designa la creacion de un nuevo producto.\n
        :param codigo: Codigo del producto
        :type codigo: int
        :param producto: Nombre del producto
        :type producto: str
        :param cantidad: Cantidad del producto
        :type cantidad: int
        :return Exception: En caso de ocurrir un error se notifica el error.
        """
        # Se toman los valores de los campos de entrada y se asignan a variables para su manipulación.
        self.valor_codigo = str(codigo.get())
        self.valor_producto = str(producto.get())
        self.valor_cantidad = str(cantidad.get())
        print("campos: ", self.valor_codigo, self.valor_producto, self.valor_cantidad)
        # Bandera para indicar si se ha producido un error
        error = False
        try:
            # Se realiza un if para ejecutar el control de caracteres en los campos de entradas.
            if validacion_alta.expresion_alta(
                self.valor_codigo, self.valor_producto, self.valor_cantidad
            ):
                # Se crea un control de datos para los campos de entrada Codigo y Cantidad.
                # Se convierten a enteros los valores para no crear conflictos.
                try:
                    self.val_codigo = int(self.valor_codigo)
                    self.val_cantidad = int(self.valor_cantidad)
                except ValueError as a:
                    print(f"Error: {a}")

                print(self.val_codigo, self.valor_producto, self.val_cantidad)

                # Se crea un nuevo producto utilizando Peewee
                nuevo_producto = Table.create(
                    codigo=self.val_codigo,
                    producto=self.valor_producto,
                    cantidad=self.val_cantidad,
                )
                nuevo_producto.save()
                print("Estoy en alta todo ok")
                # Se llama a la función que actualiza el Treeview
                self.actualizar_treeview(self.tree)
                # Se limpian los campos de entrada después que se ejecuta la acción.
                codigo.set(0)
                producto.set("-")
                cantidad.set(0)
                print(f"Producto agregado con exito: {codigo},{producto},{cantidad}")
            else:
                # Esta notificacion se introduce en este metodo de modelo y no en vista
                # porque en vista genera un error.
                notificar.mostrar_notificacion(
                    "Elementos no válidos.!\n Para Producto: Solo letras incluida la ñ, números, caracteres /, _, ' y espacios permitidos.\n"
                    "Para Cantidad: Solo números enteros y decimales separados con una coma.\n"
                    "Para número ID/Código: Solo números enteros a partir de 1."
                )
                error = True
                print("Error en campos de entrada desde metodo alta de modelo")
        except IntegrityError as b:
            error = True
            notificar.mostrar_notificacion(
                f"Error. Intente asignar otro codigo al producto.\n {b}"
            )
            print("Error de integridad desde metodo alta de modelo")

        # Si no se produce ningun error retorna True
        if not error:
            return True

    def borrar(self):
        """
        Metodo para eliminar un producto seleccionandolo en el 'Treeview'\n
        :return Exception: En caso de ocurrir un error se notifica el error.
        """
        try:

            # Toma los valores seleccionando el producto para eliminarlo completamente con sus valores.
            self.valor = self.tree.selection()
            print(self.valor)

            try:
                # Obtiene la información de la fila seleccionada y la separa en un diccionario,
                self.item = self.tree.item(self.valor)
                print(self.item)
                #  Se accede a la primera columna del ítem del Treeview en el diccionario 'item'
                self.codigo = self.item["text"]
                print("items borrar", self.codigo)

                # Busca el producto a eliminar por su código
                producto_a_eliminar = Table.get_or_none(codigo=self.codigo)

                # Verifica si el producto existe antes de intentar eliminarlo
                try:
                    # Elimina el producto de la base de datos
                    producto_a_eliminar.delete_instance()

                    # Se actualiza el Treeview luego de la acción.
                    self.actualizar_treeview(self.tree)
                except Exception as c:
                    # Informa de cualquier error durante la eliminación del producto
                    print(
                        f"Error al eliminar el producto: {c}, probablemente no exista"
                    )

            except Exception as d:
                # En caso de no detectar una selección correcta
                print(f"Error al seleccionar el producto: {d}, probablemente no exista")
        except Exception as e:
            # Informa de cualquier otro error inesperado
            print(f"Error inesperado: {e}")

    def modificar_seleccionado(self):
        """
        Metodo para modificar un producto seleccionandolo en el 'Treeview'
        Muestra dos cuadros de dialogo para insertar la modificacion:
         - Un cuadro de diálogo para ingresar el nuevo nombre.
         - Un cuadro de diálogo para ingresar la nueva cantidad.
         - Actualiza la fila seleccionada en el treeview.
        :return Exception: En caso de ocurrir un error se notifica el error.
        """
        # Obtiene la selección actual en el treeview de consulta.
        seleccion = self.tree.selection()

        try:
            # Verifica si hay una selección.
            if seleccion:
                # Obtiene la información de la fila seleccionada y la separa en un diccionario.
                item = self.tree.item(seleccion)
                # El método item() de Treeview devuelve un diccionario con información de una fila seleccionada.
                # La clave "values" en ese diccionario contiene una tupla con los valores de cada columna en esa fila.
                codigo, producto_actual, cantidad_actual = item["values"]

                nuevo_producto = simpledialog.askstring(
                    "Modificar Nombre",
                    f"Ingrese el nuevo nombre para el producto (ID: {codigo}):",
                    initialvalue=producto_actual,
                )

                # Verifica si se hizo clic en "Cancelar".
                if nuevo_producto is None:
                    return producto_actual

                nueva_cantidad = simpledialog.askinteger(
                    "Modificar Cantidad",
                    f"Ingrese la nueva cantidad para {producto_actual} (ID: {codigo}):",
                    initialvalue=cantidad_actual,
                )

                # Verifica si se hizo clic en "Cancelar".
                if nueva_cantidad is None:
                    return cantidad_actual

                self.tree.item(
                    seleccion, values=(codigo, nuevo_producto, nueva_cantidad)
                )

                # Busca el producto a modificar por su código
                producto_a_modificar = Table.get_or_none(codigo=codigo)

                # Verifica si el producto existe antes de intentar modificarlo
                if producto_a_modificar:
                    # Actualiza los valores del producto con los nuevos datos
                    producto_a_modificar.producto = nuevo_producto
                    producto_a_modificar.cantidad = nueva_cantidad
                    # Guarda los cambios en la base de datos
                    producto_a_modificar.save()

                    print("Producto modificado con éxito!")
                else:
                    # En caso de no encontrar el producto, se notifica en consola.
                    print("El producto seleccionado no existe.")
            else:
                # Se notifica en consola en caso de no haber seleccionado ningún elemento.
                print("No se ha seleccionado ningún elemento!")
        except Exception as f:
            print(f"Error en la seleccion de producto: {f}")

    def realizar_consulta(self, consulta):
        """
        Metodo para realizar una consulta a traves de una entrada de texto.\n
        :param consulta: Entrada de texto para realizar la consulta a travez de una palabra clave.
        :type consulta: str
        :return: Muestra los productos coincidentes en el 'Treeview'
        """
        try:
            # Obtiene la palabra clave de la entrada de consulta.
            # Toma la palabra clave y se convierte a minúsculas.
            # .strip() verifica si el campo de consulta no está vacío
            palabra_clave = consulta.get().lower().strip()
            print("Consulta desde modelo:", palabra_clave)
            if palabra_clave:
                # Realiza la consulta utilizando Peewee
                resultados = Table.select().where(
                    Table.producto.contains(palabra_clave)
                )
            else:
                print("No se ingreso palabra clave")
            # Variable para identificar las filas pares e impares.
            fondo_par = True
            # Verifica si hay resultados antes de intentar actualizar el treeview
            if resultados:
                # Elimina todas las filas existentes en el treeview para actualizarlo.
                for item in self.tree.get_children():
                    self.tree.delete(item)

                # Este bucle itera a través de los resultados obtenidos de la consulta a la base de datos
                # y actualiza el treeview con esos resultados
                for resultado in resultados:
                    # Convierte los valores a string antes de insertarlos en el treeview
                    self.codigo = int(resultado.codigo)
                    self.producto = str(resultado.producto)
                    self.cantidad = int(resultado.cantidad)
                    print("Valores:", self.codigo, self.producto, self.cantidad)
                    # Inserta una nueva fila en el treeview con los valores del producto actual.
                    self.tree.insert(
                        "",
                        "end",
                        text=resultado,
                        values=(
                            resultado.codigo,
                            resultado.producto,
                            resultado.cantidad,
                        ),
                        tags=(
                            "odd"
                            if fondo_par
                            or isinstance(resultado.codigo, int)
                            and resultado.codigo % 2 == 0
                            else "even"
                        ),
                    )
                    # Alterna el fondo para la próxima fila.
                    fondo_par = not fondo_par
                # Agrega los colores de fondo para las filas impares y pares.
                self.tree.tag_configure(
                    "odd", background="#E8E8E8"
                )  # Fondo gris claro.
                self.tree.tag_configure("even", background="white")  # Fondo blanco.
                # Se limpia el campo de entrada después que se ejecuta la acción.
                consulta.set("")
            else:
                # Esta notificacion se introduce en este metodo de modelo y no en vista
                # porque en vista genera un error.
                notificar.mostrar_notificacion("No se encontro ningun producto")
                # Si no hay resultados, muestra una notificación en consola
                print("No se encontraron productos para la consulta.")

        # Entra en este bloque cuando ocurre una excepción de cualquier tipo. y Asigna la instancia a la variable e para ser utilizada.
        except Exception as g:
            # Se le notifica al usuario en caso de error y se muestran detalles del error.
            print(f"Hubo un error: {g}")

    # Metodo para mostrar el inventario actualizado en el treeview, ya sea creado o modificado.
    def actualizar_treeview(self, tree):
        """
        Metodo para acttualizar las filas del 'Treeview'.\n
        Se llama este metodo de diferentes formas:
         - Al iniciar la aplicacion se actualizan las filas del 'Treeview' con datos que contenga la base de datos.
         - Al realizar una operacion 'CRUD'.
         - Al hacer click en el boton en pantalla 'Actualizar'.
        """
        try:
            # Elimina todas las filas existentes en el treeview para actualizarlo.
            for item in tree.get_children():
                tree.delete(item)

            # Selecciona todos los registros de la tabla 'Table'.
            productos = Table.select().order_by(Table.codigo.desc())

            # Variable para identificar las filas pares e impares.
            fondo_par = True

            # Itera sobre cada producto y lo agrega al treeview.
            for producto in productos:
                # Inserta una nueva fila en el treeview con los valores del producto actual.
                tree.insert(
                    "",  # El primer argumento es el ID.
                    0,  # El segundo argumento es la posición donde se insertará la nueva fila.
                    text=producto.codigo,
                    # Los valores de las columnas para la nueva fila.
                    values=(producto.codigo, producto.producto, producto.cantidad),
                    # Etiqueta que determina el color de fondo de la fila.
                    tags=("odd" if fondo_par else "even"),
                )
                # Alterna el fondo para la próxima fila.
                fondo_par = not fondo_par

            # Agrega los colores de fondo para las filas impares y pares.
            tree.tag_configure("odd", background="#E8E8E8")  # Fondo gris claro.
            tree.tag_configure("even", background="white")  # Fondo blanco.
        except Exception as h:
            # Manejo de cualquier excepción que pueda ocurrir durante la ejecución.
            print(f"Error al actualizar el Treeview: {h}")
