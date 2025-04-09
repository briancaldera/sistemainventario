import tkinter as tk
from decimal import Decimal
from tkinter import Frame, Label, LabelFrame, Scrollbar, Button, VERTICAL, RIGHT, Y, HORIZONTAL, BOTTOM, X, BOTH
from tkinter import ttk, messagebox
from typing import TypedDict

from model.compra import Compra
from model.producto import Producto
from model.proveedor import ProveedorAR
from screens.DetallesWindow import DetallesWindow
from services.MercadeoService import MercadeoService
from services.ProductoService import ProductoService

Cesta = list[TypedDict('Cesta', {'producto': Producto, 'cantidad': int})]


class Compras(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.catalogo: list[Producto] = []
        self.cesta: Cesta = []
        self.proveedor: ProveedorAR | None = None

        self.numero_compra_actual = self.obtener_numero_compra_actual()
        self.productos_service = ProductoService()
        self.mercadeo_service = MercadeoService()

        self.widgets()
        self.mostrar_numero_compra()
        self.controller = controller

    def widgets(self):

        frame1 = tk.Frame(self, bg="#dddddd", highlightbackground="gray", highlightthickness=1)
        frame1.pack()
        frame1.place(x=0, y=0, width=1100, height=100)

        titulo = tk.Label(self, text="COMPRAS", font=("Arial", 20), bg="#dddddd", anchor="center")
        titulo.pack()
        titulo.place(x=5, y=0, width=1090, height=90)

        frame2 = tk.Frame(self, bg="#C6D9E3", highlightbackground="gray", highlightthickness=1)
        frame2.place(x=0, y=100, width=1100, height=550)

        Lblframe = LabelFrame(frame2, text="Datos de la compra", font=("Arial", 12), bg="#C6D9E3", fg="black")
        Lblframe.place(x=10, y=10, width=1060, height=80)

        label_numero_factura = Label(Lblframe, text="Número de \nfactura", font=("Arial", 12), bg="#C6D9E3", fg="black")
        label_numero_factura.place(x=10, y=5)
        self.numero_compra = tk.StringVar()

        self.entry_numero_compra = ttk.Entry(Lblframe, textvariable=self.numero_compra, state="readonly",
                                             font=("Arial", 12))
        self.entry_numero_compra.place(x=100, y=5, width=80)

        label_nombre = tk.Label(Lblframe, text="productos: ", font=("Arial", 12), bg="#C6D9E3", fg="black")
        label_nombre.place(x=200, y=12)

        self.entry_nombre = ttk.Combobox(Lblframe, font=("Arial", 12), state="readonly")
        self.entry_nombre.place(x=280, y=10, width=180)
        self.refrescar_productos()

        label_valor = tk.Label(Lblframe, text="Precio: ", font=("Arial", 12), bg="#C6D9E3")
        label_valor.place(x=470, y=12)

        self.entry_valor = ttk.Entry(Lblframe, font=("Arial", 12), state="readonly")
        self.entry_valor.place(x=540, y=10, width=180)

        self.entry_nombre.bind("<<ComboboxSelected>>", self.actualizar_costo)

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

        boton_facturas = Button(lblframe1, text="Ver Compras", font=("Arial", 12), bg="#f4b400",
                                command=self.abrir_ventana_factura)
        boton_facturas.place(x=750, y=10, width=240, height=50)

        self.label_suma_total = tk.Label(frame2, text="Total: ", font=("Arial", 12), bg="#C6D9E3")
        self.label_suma_total.place(x=360, y=335)

        self.proveedor_info_frame = tk.Frame(treframe, bg="#C6D9E3")

        # Use a dropdown to show the name of the Proveedores, and set the self.proveedor to the selected Proveedor on selection
        self.proveedores_combobox = ttk.Combobox(self.proveedor_info_frame, font=("Arial", 12), state="readonly")
        self.proveedores_combobox.pack(fill=BOTH)

        self.refrescar_proveedores()
        self.proveedores_combobox.bind("<<ComboboxSelected>>", self.actualizar_proveedor)

        self.proveedor_nombre_label = tk.Label(self.proveedor_info_frame, text="Nombre: ", font=("Arial", 12),
                                               bg="#C6D9E3")
        self.proveedor_nombre_label.pack(fill=BOTH)

        self.proveedor_direccion_label = tk.Label(self.proveedor_info_frame, text="Direccion: ", font=("Arial", 12),
                                                  bg="#C6D9E3")
        self.proveedor_direccion_label.pack(fill=BOTH)

        self.proveedor_telefono_label = tk.Label(self.proveedor_info_frame, text="Telefono: ", font=("Arial", 12),
                                                 bg="#C6D9E3")
        self.proveedor_telefono_label.pack(fill=BOTH)
        self.proveedor_info_frame.place(x=550, y=0, width=300, height=200)

    def refrescar_proveedores(self):
        proveedores = ProveedorAR.select()
        self.proveedores_combobox["values"] = [proveedor.nombre for proveedor in proveedores]

    def actualizar_proveedor(self, event):
        nombre_proveedor = self.proveedores_combobox.get()
        self.proveedor = ProveedorAR.select().where(ProveedorAR.nombre == nombre_proveedor).get()
        self.refrescar_proveedor()

    def refrescar_proveedor(self):
        if self.proveedor:
            self.proveedor_nombre_label.config(text=f"Nombre: {self.proveedor.nombre}")
            self.proveedor_direccion_label.config(text=f"Direccion: {self.proveedor.direccion}")
            self.proveedor_telefono_label.config(text=f"Telefono: {self.proveedor.telefono}")
        else:
            self.proveedor_nombre_label.config(text=f"Nombre: ")
            self.proveedor_direccion_label.config(text=f"Direccion: ")
            self.proveedor_telefono_label.config(text=f"Telefono: ")

    def refrescar_productos(self):
        self.catalogo = self.productos_service.listar()
        self.entry_nombre["values"] = [producto.nombre for producto in self.catalogo]

    def actualizar_costo(self, event):
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
            cantidad = int(cantidad)
            producto_encontrado = [x for x in self.catalogo if x.nombre == producto][0]

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

        else:
            messagebox.showerror("Error", "Por favor complete los campos")

    def obtener_total(self):
        total = 0.0
        for child in self.tree.get_children():
            subtotal = float(self.tree.item(child, "values")[3])
            total += subtotal
        return total

    def abrir_ventana_pago(self):
        if not self.proveedor:
            messagebox.showerror("Error", "Por favor seleccione un proveedor")
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

        # boton_calcular = tk.Button(ventana_pago, text="Calcular Cambio", font=("Arial", 12), bg="white",
        #                            command=calcular_cambio)
        # boton_calcular.place(x=100, y=240, width=240, height=40)

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
            producto = {'producto_id': item['producto'].producto_id, 'cantidad': item['cantidad']}

            lista_productos.append(producto)

        request = MercadeoService.CompraRequest(proveedor_id=self.proveedor.id, costo_total=cantidad_pagada,
            lista_producto=lista_productos)

        try:
            self.mercadeo_service.comprar(request)
            messagebox.showinfo('Compra registrada', 'Compra registrada exitosamente')
            self.refrescar_productos()

        except Exception as e:
            messagebox.showerror('Error', 'Ocurrió un error al intentar registrar la compra')
            print(e)

            self.numero_compra_actual += 1
            self.mostrar_numero_compra()

            for child in self.tree.get_children():
                self.tree.delete(child)
            self.label_suma_total.config(text="Total: 0.0")

            ventana_pago.destroy()

    def obtener_numero_compra_actual(self):
        max_compra = Compra.select(Compra.numero_compra).order_by(Compra.numero_compra.desc()).limit(1)
        return max_compra.get().numero_compra + 1 if max_compra.exists() else 1

    def mostrar_numero_compra(self):
        self.numero_compra.set(self.numero_compra_actual)

    def abrir_ventana_factura(self):
        VentanaCompras(self)


class VentanaCompras(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.compras: list[Compras] = []
        self.mercadeo_service = MercadeoService()

        self.title("Compras")
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

        tree_facturas = ttk.Treeview(treframe, columns=("ID", "Numero de compra", "Proveedor", "Costo total", 'Fecha'),
                                     show="headings", yscrollcommand=Scrol_y.set, xscrollcommand=Scrol_x.set)

        self.tree_compras = tree_facturas
        Scrol_y.config(command=tree_facturas.yview)
        Scrol_x.config(command=tree_facturas.xview)

        tree_facturas.heading("#1", text="ID")
        tree_facturas.heading("#2", text="Numero de compra")
        tree_facturas.heading("#3", text="Proveedor")
        tree_facturas.heading("#4", text="Costo total")
        tree_facturas.heading("#5", text="Fecha")

        tree_facturas.column("ID", width=70, anchor="center")
        tree_facturas.column("Numero de compra", width=100, anchor="center")
        tree_facturas.column("Proveedor", width=200, anchor="center")
        tree_facturas.column("Costo total", width=130, anchor="center")
        tree_facturas.column("Fecha", width=130, anchor="center")

        tree_facturas.pack(fill=BOTH, expand=True)

        tree_facturas.bind('<<TreeviewSelect>>', self.on_compra_seleccion)
        self.refrescar_compras()

    def refrescar_compras(self):
        compras = self.mercadeo_service.listar_compras()

        self.tree_compras.delete(*self.tree_compras.get_children())

        for compra in compras:
            # Insert each venta in the self.tree_ventas considering the columns

            proveedor = ProveedorAR.get_by_id(compra.proveedor_id)

            self.tree_compras.insert("", 0, text=compra.compra_id, values=(
                compra.compra_id, compra.numero_compra, proveedor.nombre, compra.costo_total, compra.fecha))

    def on_compra_seleccion(self, event):

        seleccion = self.tree_compras.selection()

        if len(seleccion) == 0:
            return

        index = seleccion[0]

        item = self.tree_compras.item(index)

        compra_id = item['values'][0]

        compra = Compra.get_by_id(compra_id)

        DetallesWindow(self, compra)
