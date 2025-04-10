import sqlite3
import tkinter as tk
from decimal import Decimal
from tkinter import *
from tkinter import ttk, messagebox
from typing import TypedDict

from model.cliente import ClienteAR
from model.compra import Compra
from model.producto import Producto
from model.proveedor import Proveedor, ProveedorAR
from model.venta import Venta, Egreso
from screens.DetallesWindow import DetallesWindow
from services.MercadeoService import MercadeoService
from services.ProductoService import ProductoService

Cesta = list[TypedDict('Cesta', {'producto': Producto, 'cantidad': int})]


class Ventas(tk.Frame):
    db_name = "database.db"

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.catalogo: list[Producto] = []
        self.cesta: Cesta = []
        self.cliente: ClienteAR | None = None

        self.numero_factura_actual = self.obtener_numero_factura_actual()
        self.productos_service = ProductoService()
        self.mercadeo_service = MercadeoService()

        self.widgets()
        self.mostrar_numero_factura()
        self.controller = controller

    def widgets(self):

        frame1 = tk.Frame(self, bg="#dddddd", highlightbackground="gray", highlightthickness=1)
        frame1.pack()
        frame1.place(x=0, y=0, width=1100, height=100)

        titulo = tk.Label(self, text="VENTAS", font=("Arial", 20), bg="#dddddd", anchor="center")
        titulo.pack()
        titulo.place(x=5, y=0, width=1090, height=90)

        frame2 = tk.Frame(self, bg="#C6D9E3", highlightbackground="gray", highlightthickness=1)
        frame2.place(x=0, y=100, width=1100, height=550)

        Lblframe = LabelFrame(frame2, text="Datos de la venta", font=("Arial", 12), bg="#C6D9E3", fg="black")
        Lblframe.place(x=10, y=10, width=1060, height=80)

        label_numero_factura = Label(Lblframe, text="Número de \nfactura", font=("Arial", 12), bg="#C6D9E3", fg="black")
        label_numero_factura.place(x=10, y=5)
        self.numero_factura = tk.StringVar()

        self.entry_numero_factura = ttk.Entry(Lblframe, textvariable=self.numero_factura, state="readonly",
                                              font=("Arial", 12))
        self.entry_numero_factura.place(x=100, y=5, width=80)

        label_nombre = tk.Label(Lblframe, text="productos: ", font=("Arial", 12), bg="#C6D9E3", fg="black")
        label_nombre.place(x=200, y=12)

        self.entry_nombre = ttk.Combobox(Lblframe, font=("Arial", 12), state="readonly")
        self.entry_nombre.place(x=280, y=10, width=180)
        self.refrescar_productos()

        label_valor = tk.Label(Lblframe, text="Precio: ", font=("Arial", 12), bg="#C6D9E3")
        label_valor.place(x=470, y=12)

        self.entry_valor = ttk.Entry(Lblframe, font=("Arial", 12), state="readonly")
        self.entry_valor.place(x=540, y=10, width=180)

        self.entry_nombre.bind("<<ComboboxSelected>>", self.actualizar_precio)

        label_cantidad = tk.Label(Lblframe, text="Cantidad: ", font=("Arial", 12), bg="#C6D9E3")
        label_cantidad.place(x=730, y=12)
        self.entry_cantidad = ttk.Entry(Lblframe, font=("Arial", 12))
        self.entry_cantidad.place(x=820, y=10)

        treframe = tk.Frame(frame2, bg="#C6D9E3")
        treframe.place(x=150, y=120, width=800, height=200)

        Scrol_y = Scrollbar(treframe, orient=VERTICAL)
        Scrol_y.pack(side=RIGHT, fill=Y)

        Scrol_x = Scrollbar(treframe, orient=HORIZONTAL)
        Scrol_x.pack(side=BOTTOM, fill=X)

        self.tree = ttk.Treeview(treframe, columns=("Producto", "Precio", "Cantidad", "subtotal"), show="headings",
                                 yscrollcommand=Scrol_y.set, xscrollcommand=Scrol_x.set)
        Scrol_y.config(command=self.tree.yview)
        Scrol_x.config(command=self.tree.xview)

        self.tree.heading("#1", text="Producto")
        self.tree.heading("#2", text="Precio")
        self.tree.heading("#3", text="Cantidad")
        self.tree.heading("#4", text="Subtotal")

        self.tree.column("Producto", anchor="center")
        self.tree.column("Precio", anchor="center")
        self.tree.column("Cantidad", anchor="center")
        self.tree.column("subtotal", anchor="center")

        self.tree.pack(fill=BOTH, expand=True)

        lblframe1 = LabelFrame(frame2, text="opciones", font=("Arial", 12), bg="#C6D9E3")
        lblframe1.place(x=10, y=380, width=1060, height=100)

        boton_agregar = Button(lblframe1, text="Agregar articulo", font=("Arial", 12), bg="#f4b400",
                               command=self.agregar_a_la_cesta)
        boton_agregar.place(x=50, y=10, width=240, height=50)

        boton_pagar = Button(lblframe1, text="Pagar", font=("Arial", 12), bg="#f4b400", command=self.abrir_ventana_pago)
        boton_pagar.place(x=400, y=10, width=240, height=50)

        boton_facturas = Button(lblframe1, text="Ver Facturas", font=("Arial", 12), bg="#f4b400",
                                command=self.abrir_ventana_factura)
        boton_facturas.place(x=750, y=10, width=240, height=50)

        self.label_suma_total = tk.Label(frame2, text="Total: ", font=("Arial", 12), bg="#C6D9E3")
        self.label_suma_total.place(x=360, y=335)

        self.cliente_info_frame = tk.Frame(treframe, bg="#C6D9E3")
        # self.cliente_info_frame.pack(fill=BOTH)

        self.cliente_cedula_entry = Entry(self.cliente_info_frame, font=("Arial", 12))
        self.cliente_cedula_entry.pack(fill=BOTH)

        self.buscar_cedula = Button(self.cliente_info_frame, text='Buscar', font=("Arial", 12), bg="white",
                                    command=self.buscar_cliente)
        self.buscar_cedula.pack(fill=BOTH)


        self.cliente_nombre_label = tk.Label(self.cliente_info_frame, text="Nombre: ", font=("Arial", 12), bg="#C6D9E3")
        self.cliente_nombre_label.pack(fill=BOTH)

        self.cliente_direccion_label = tk.Label(self.cliente_info_frame, text="Direccion: ", font=("Arial", 12),
                                                bg="#C6D9E3")
        self.cliente_direccion_label.pack(fill=BOTH)

        self.cliente_telefono_label = tk.Label(self.cliente_info_frame, text="Telefono: ", font=("Arial", 12),
                                               bg="#C6D9E3")
        self.cliente_telefono_label.pack(fill=BOTH)
        self.cliente_info_frame.place(x=550, y=0, width=300, height=200)


    def buscar_cliente(self):
        cedula = self.cliente_cedula_entry.get()
        if cedula:
            cliente = ClienteAR.select().where(ClienteAR.cedula == cedula).get_or_none()
            if cliente:
                self.cliente = cliente
                self.refrescar_cliente()
            else:
                messagebox.showerror("Error", "Cliente no encontrado")
        else:
            messagebox.showerror("Error", "Por favor ingrese una cedula")

    def refrescar_cliente(self):
        if self.cliente:

            self.cliente_nombre_label.config(text=f"Nombre: {self.cliente.nombre}")
            self.cliente_direccion_label.config(text=f"Direccion: {self.cliente.direccion}")
            self.cliente_telefono_label.config(text=f"Telefono: {self.cliente.telefono}")
        else:

            self.cliente_nombre_label.config(text=f"Nombre: ")
            self.cliente_direccion_label.config(text=f"Direccion: ")
            self.cliente_telefono_label.config(text=f"Telefono: ")

    def refrescar_productos(self):
        self.catalogo = self.productos_service.listar()
        self.entry_nombre["values"] = [producto.nombre for producto in self.catalogo]

    def actualizar_precio(self, event):
        nombre_producto = self.entry_nombre.get()

        producto = [x for x in self.catalogo if x.nombre == nombre_producto][0]
        precio = producto.precio

        self.entry_valor.config(state="normal")
        self.entry_valor.delete(0, tk.END)
        self.entry_valor.insert(0, precio)
        self.entry_valor.config(state="readonly")

    def actualizar_total(self):
        total = 0.0
        for child in self.tree.get_children():
            subtotal = float(self.tree.item(child, "values")[3])
            total += subtotal
        self.label_suma_total.config(text=f"Total: {total}")

    def agregar_a_la_cesta(self):
        producto = self.entry_nombre.get()
        precio = self.entry_valor.get()
        cantidad = self.entry_cantidad.get()

        if producto and precio and cantidad:
            try:
                cantidad = int(cantidad)

                # check producto stock and show message if not enough stock
                producto_encontrado = [x for x in self.catalogo if x.nombre == producto][0]
                if producto_encontrado.existencia < cantidad:
                    messagebox.showerror("Error", f"No hay suficientes existencias de {producto}")
                    return

                precio = float(precio)
                subtotal = precio * cantidad

                self.cesta.append({'producto': producto_encontrado, 'cantidad': cantidad})

                self.tree.insert("", "end", values=(producto, f"{precio: .2f}", cantidad, f"{subtotal: .2f}"))

                self.entry_nombre.set("")
                self.entry_valor.config(state="normal")
                self.entry_valor.delete(0, tk.END)
                self.entry_valor.config(state="readonly")
                self.entry_cantidad.delete(0, tk.END)

                self.actualizar_total()
            except ValueError:
                messagebox.showerror("Error", "Cantidad no valida")
        else:
            messagebox.showerror("Error", "Por favor complete los campos")

    def obtener_total(self):
        total = 0.0
        for child in self.tree.get_children():
            subtotal = float(self.tree.item(child, "values")[3])
            total += subtotal
        return total

    def abrir_ventana_pago(self):
        if not self.cliente:
            messagebox.showerror("Error", "Por favor seleccione un cliente")
            return

        if not self.tree.get_children():
            messagebox.showerror("Error", "No hay productos para pagar")
            return

        total = self.obtener_total()
        ventana_pago = tk.Toplevel(self)
        ventana_pago.title("Realizar Pago")
        ventana_pago.geometry("400x400")
        ventana_pago.resizable(False, False)
        ventana_pago.config(bg="#C6D9E3")

        label_total = tk.Label(ventana_pago, text=f"Total a pagar: {self.obtener_total()}", font=("Arial", 12),
                               bg="#C6D9E3")
        label_total.place(x=70, y=20)

        label_cantidad_pagada = tk.Label(ventana_pago, text="Cantidad pagada: ", font=("Arial", 12), bg="#C6D9E3")
        label_cantidad_pagada.place(x=100, y=90)
        entry_cantidad_pagada = ttk.Entry(ventana_pago, font=("Arial", 12))
        entry_cantidad_pagada.place(x=100, y=130)

        label_cambio = tk.Label(ventana_pago, text="", font=("Arial", 12), bg="#C6D9E3")
        label_cambio.place(x=100, y=190)

        def calcular_cambio():
            try:
                cantidad_pagada = float(entry_cantidad_pagada.get())
                total = self.obtener_total()
                cambio = cantidad_pagada - total
                if cambio < 0:
                    messagebox.showerror("Error", "La cantidad pagada es insuficiente")
                    return
                label_cambio.config(text=f"Cambio: {cambio}")
            except ValueError:
                messagebox.showerror("Error", "Cantidad no valida")

        boton_calcular = tk.Button(ventana_pago, text="Calcular Cambio", font=("Arial", 12), bg="white",
                                   command=calcular_cambio)
        boton_calcular.place(x=100, y=240, width=240, height=40)

        boton_pagar = tk.Button(ventana_pago, text="Pagar", font=("Arial", 12), bg="white",
                                command=lambda: self.pagar(ventana_pago, entry_cantidad_pagada, label_cambio))
        boton_pagar.place(x=100, y=300, width=240, height=40)

    def pagar(self, ventana_pago, entry_cantidad_pagada, label_cambio):
        cantidad_pagada = entry_cantidad_pagada.get()
        total = self.obtener_total()
        cambio = Decimal(cantidad_pagada) - Decimal(total)

        if cambio < 0:
            messagebox.showerror("Error", "La cantidad pagada es insuficiente")
            return

        lista_productos = []

        for item in self.cesta:
            producto = {
                'producto_id': item['producto'].producto_id,
                'cantidad': item['cantidad']
            }

            lista_productos.append(producto)

        request = MercadeoService.VentaRequest(
            cliente_id=self.cliente.id,
            total_neto=str(total),
            total_pagado=cantidad_pagada,
            lista_producto=lista_productos
        )

        try:
            self.mercadeo_service.vender(request)
            messagebox.showinfo('Venta registrada', 'Venta registrada exitosamente')
            self.refrescar_productos()

        except Exception as e:
            messagebox.showerror('Error', 'Ocurrió un error al intentar registrar la venta')
            print(e)

            self.numero_factura_actual += 1
            self.mostrar_numero_factura()

            for child in self.tree.get_children():
                self.tree.delete(child)
            self.label_suma_total.config(text="Total: 0.0")

            ventana_pago.destroy()

    def obtener_numero_factura_actual(self):

        max_factura = Venta.select(Venta.numero_factura).order_by(Venta.numero_factura.desc()).limit(1)

        return max_factura.get().numero_compra + 1 if max_factura.exists() else 1

    def mostrar_numero_factura(self):
        self.numero_factura.set(self.numero_factura_actual)

    def abrir_ventana_factura(self):

        VentanaVentas(self)
        return
        ventana_facturas = Toplevel(self)
        ventana_facturas.title("Factura")
        ventana_facturas.geometry("800x500")
        ventana_facturas.resizable(False, False)
        ventana_facturas.config(bg="#C6D9E3")

        facturas = Label(ventana_facturas, bg="#C6D9E3", text="Facturas registradas", font=("Arial", 20))
        facturas.place(x=150, y=15)

        treframe = Frame(ventana_facturas, bg="#C6D9E3")
        treframe.place(x=10, y=100, width=780, height=380)

        Scrol_y = Scrollbar(treframe, orient=VERTICAL)
        Scrol_y.pack(side=RIGHT, fill=Y)

        Scrol_x = Scrollbar(treframe, orient=HORIZONTAL)
        Scrol_x.pack(side=BOTTOM, fill=X)

        tree_facturas = ttk.Treeview(treframe, columns=("ID", "Factura", "Producto", "Precio", "cantidad", "Subtotal"),
                                     show="headings", yscrollcommand=Scrol_y.set, xscrollcommand=Scrol_x.set)
        Scrol_y.config(command=tree_facturas.yview)
        Scrol_x.config(command=tree_facturas.xview)

        tree_facturas.heading("#1", text="ID")
        tree_facturas.heading("#2", text="Factura")
        tree_facturas.heading("#3", text="Producto")
        tree_facturas.heading("#4", text="Precio")
        tree_facturas.heading("#5", text="cantidad")
        tree_facturas.heading("#6", text="Subtotal")

        tree_facturas.column("ID", width=70, anchor="center")
        tree_facturas.column("Factura", width=100, anchor="center")
        tree_facturas.column("Producto", width=200, anchor="center")
        tree_facturas.column("Precio", width=130, anchor="center")
        tree_facturas.column("cantidad", width=130, anchor="center")
        tree_facturas.column("Subtotal", width=130, anchor="center")

        tree_facturas.pack(fill=BOTH, expand=True)

        self.cargar_facturas(tree_facturas)

    def cargar_facturas(self, tree):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT * FROM ventas")
            facturas = c.fetchall()
            for factura in facturas:
                tree.insert("", "end", values=factura)
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al cargar facturas: {e}")


class VentanaVentas(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.mercadeo_service = MercadeoService()
        self.ventas: list[Ventas] = []
        self.title("Ventas")
        self.geometry("800x500")
        self.resizable(False, False)
        self.config(bg="#C6D9E3")

        facturas = Label(self, bg="#C6D9E3", text="Facturas registradas", font=("Arial", 20))
        facturas.place(x=150, y=15)

        treframe = Frame(self, bg="#C6D9E3")
        treframe.place(x=10, y=100, width=780, height=380)

        Scrol_y = Scrollbar(treframe, orient=VERTICAL)
        Scrol_y.pack(side=RIGHT, fill=Y)

        Scrol_x = Scrollbar(treframe, orient=HORIZONTAL)
        Scrol_x.pack(side=BOTTOM, fill=X)

        tree_facturas = ttk.Treeview(treframe, columns=("ID", "Factura", "Cliente", "Precio", "Subtotal", 'Fecha'),
                                     show="headings", yscrollcommand=Scrol_y.set, xscrollcommand=Scrol_x.set)

        self.tree_ventas = tree_facturas
        Scrol_y.config(command=tree_facturas.yview)
        Scrol_x.config(command=tree_facturas.xview)

        tree_facturas.heading("#1", text="ID")
        tree_facturas.heading("#2", text="Factura")
        tree_facturas.heading("#3", text="Cliente")
        tree_facturas.heading("#4", text="Precio")
        tree_facturas.heading("#5", text="Subtotal")
        tree_facturas.heading("#6", text="Fecha")

        tree_facturas.column("ID", width=70, anchor="center")
        tree_facturas.column("Factura", width=100, anchor="center")
        tree_facturas.column("Cliente", width=200, anchor="center")
        tree_facturas.column("Precio", width=130, anchor="center")
        tree_facturas.column("Subtotal", width=130, anchor="center")
        tree_facturas.column("Fecha", width=130, anchor="center")

        tree_facturas.pack(fill=BOTH, expand=True)

        tree_facturas.bind('<<TreeviewSelect>>', self.on_venta_seleccion)
        self.refrescar_ventas()

    def refrescar_ventas(self):
        ventas = self.mercadeo_service.listar_ventas()

        for item in self.tree_ventas.get_children():
            self.tree_ventas.delete(item)

        for venta in ventas:
            # Insert each venta in the self.tree_ventas considering the columns

            cliente = ClienteAR.get_by_id(venta.cliente_id)

            self.tree_ventas.insert("", 0, text=venta.venta_id, values=(
                venta.venta_id, venta.numero_factura, cliente.nombre, venta.total_neto, venta.total_pagado,
                venta.fecha))

    def on_venta_seleccion(self, event):

        seleccion = self.tree_ventas.selection()

        if len(seleccion) == 0:
            return

        index = seleccion[0]

        item = self.tree_ventas.item(index)

        venta_id = item['values'][0]

        venta = Venta.get_by_id(venta_id)

        DetallesWindow(self, venta)
