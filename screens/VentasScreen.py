import sqlite3
import tkinter as tk
from decimal import Decimal
from tkinter import *
from tkinter import ttk, messagebox
from typing import TypedDict
from model.cliente import ClienteAR
from model.producto import Producto
from model.venta import Venta
from screens.DetallesWindow import DetallesWindow
from services.MercadeoService import MercadeoService
from services.ProductoService import ProductoService
from services.ReferenciaService import ReferenciaService
from PIL import Image, ImageTk
import os
from utils.fs_util import get_resource_path

Cesta = list[TypedDict('Cesta', {'producto': Producto, 'cantidad': int})]


class Ventas(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.catalogo: list[Producto] = []
        self.cesta: Cesta = []
        self.cliente: ClienteAR | None = None

        self.referencia_service = ReferenciaService()
        self.referencia = self.referencia_service.conseguir_ultima_referencia()

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

        self.label_total_bolivares = tk.Label(frame2, text="Total: Bs.D", font=("Arial", 12), bg="#C6D9E3")
        self.label_total_bolivares.place(x=660, y=335)

        self.label_referencia = tk.Label(frame2,
                                         text=f"Referencia: {self.referencia.valor if self.referencia is not None else 'Sin referencia'}",
                                         font=("Arial", 12), bg="#C6D9E3")
        self.label_referencia.place(x=160, y=335)

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
                messagebox.showerror("Error", "Cliente no encontrado", parent=self)
        else:
            messagebox.showerror("Error", "Por favor ingrese una cedula", parent=self)

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

        if self.referencia is None:
            self.label_total_bolivares.config(text=f'Total: Sin referencia')
        else:
            self.label_total_bolivares.config(text=f'Total: Bs. D {Decimal(str(total)) * self.referencia.valor}')


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
                    messagebox.showerror("Error", f"No hay suficientes existencias de {producto}", parent=self)
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
                messagebox.showerror("Error", "Cantidad no valida", parent=self)
        else:
            messagebox.showerror("Error", "Por favor complete los campos", parent=self)

    def obtener_total(self):
        total = 0.0
        for child in self.tree.get_children():
            subtotal = float(self.tree.item(child, "values")[3])
            total += subtotal
        return total

    def abrir_ventana_pago(self):
        if not self.cliente:
            messagebox.showerror("Error", "Por favor seleccione un cliente", parent=self)
            return

        if not self.tree.get_children():
            messagebox.showerror("Error", "No hay productos para pagar", parent=self)
            return

        if self.referencia is None:
            messagebox.showerror("Error", "No hay referencia disponible. Debe crear un referencia de cambio", parent=self)
            return

        ventana_pago = tk.Toplevel(self)
        ventana_pago.title("Realizar Pago")
        ventana_pago.geometry("400x400")
        ventana_pago.resizable(False, False)
        ventana_pago.config(bg="#C6D9E3")

        total = self.obtener_total()
        ref = self.referencia

        label_referencia = tk.Label(ventana_pago,
                                    text=f"Referencia: {ref.valor if ref is not None else 'Sin referencia'}",
                                    font=("Arial", 12),
                                    bg="#C6D9E3")
        label_referencia.place(x=70, y=10)

        label_total = tk.Label(ventana_pago, text=f"Total a pagar: {total}", font=("Arial", 12), bg="#C6D9E3")
        label_total.place(x=70, y=30)

        label_total_bolivares = tk.Label(ventana_pago,
                                         text=f"Total a pagar en Bolívares: {Decimal(str(total)) * ref.valor if ref is not None else 'Sin referencia'}",
                                         font=("Arial", 12),
                                         bg="#C6D9E3")
        label_total_bolivares.place(x=70, y=60)

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
                    # make ventana_pago be parent of messagebox
                    messagebox.showerror("Error", "La cantidad pagada es insuficiente", parent=ventana_pago)
                    return
                label_cambio.config(text=f"Cambio: {cambio}")
            except ValueError:
                messagebox.showerror("Error", "Cantidad no valida", parent=ventana_pago)

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
            messagebox.showerror("Error", "La cantidad pagada es insuficiente", parent=ventana_pago)
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
            lista_producto=lista_productos,
            referencia_id = self.referencia.referencia_id
        )

        try:
            self.mercadeo_service.vender(request)
            messagebox.showinfo('Venta registrada', 'Venta registrada exitosamente', parent=ventana_pago)
            self.refrescar_productos()

        except Exception as e:
            messagebox.showerror('Error', 'Ocurrió un error al intentar registrar la venta', parent=ventana_pago)
            print(e)

            self.numero_factura_actual += 1
            self.mostrar_numero_factura()

            for child in self.tree.get_children():
                self.tree.delete(child)
            self.label_suma_total.config(text="Total: 0.0")

            ventana_pago.destroy()

    def obtener_numero_factura_actual(self):

        max_factura = Venta.select(Venta.numero_factura).order_by(Venta.numero_factura.desc()).limit(1)

        return max_factura.get().numero_factura + 1 if max_factura.exists() else 1

    def mostrar_numero_factura(self):
        self.numero_factura.set(self.numero_factura_actual)

    def abrir_ventana_factura(self):
        VentanaVentas(self)

class VentanaVentas(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.mercadeo_service = MercadeoService()
        self.ventas: list[Ventas] = []
        self.title("Ventas")
        self.geometry("800x550")
        self.resizable(False, False)
        self.config(bg="#C6D9E3")

        images_folder = get_resource_path('imagenes')
        image_path = os.path.join(images_folder, "artvinil.png")

        header_frame = Frame(self, bg="#C6D9E3")
        header_frame.pack(fill='x')

        self.logo_image = Image.open(image_path)
        self.logo_image = self.logo_image.resize((150, 150))
        self.logo_image = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = Label(header_frame, image=self.logo_image, bg="#C6D9E3")
        self.logo_label.pack(pady=10)

        # align titulo to the top right of the window
        titulo_label = Label(header_frame, text="Reporte de facturas de ventas", font=("Arial", 16), bg="#C6D9E3")
        titulo_label.pack(pady=10)

        # Campos de búsqueda
        frame_busqueda = Frame(self, bg="#C6D9E3")
        frame_busqueda.pack(fill=X, padx=10, pady=5)

        label_buscar_cliente = Label(frame_busqueda, text="Cliente:", bg="#C6D9E3", font=("Arial", 12))
        label_buscar_cliente.pack(side=LEFT, padx=5)
        self.entry_buscar_cliente = ttk.Entry(frame_busqueda, font=("Arial", 12))
        self.entry_buscar_cliente.pack(side=LEFT, padx=5)
        self.entry_buscar_cliente.bind("<KeyRelease>", self.buscar_venta)

        label_buscar_fecha = Label(frame_busqueda, text="Fecha:", bg="#C6D9E3", font=("Arial", 12))
        label_buscar_fecha.pack(side=LEFT, padx=5)
        self.entry_buscar_fecha = ttk.Entry(frame_busqueda, font=("Arial", 12))
        self.entry_buscar_fecha.pack(side=LEFT, padx=5)
        self.entry_buscar_fecha.bind("<KeyRelease>", self.buscar_venta)

        label_buscar_factura = Label(frame_busqueda, text="Factura #:", bg="#C6D9E3", font=("Arial", 12))
        label_buscar_factura.pack(side=LEFT, padx=5)
        self.entry_buscar_factura = ttk.Entry(frame_busqueda, font=("Arial", 12))
        self.entry_buscar_factura.pack(side=LEFT, padx=5)
        self.entry_buscar_factura.bind("<KeyRelease>", self.buscar_venta)

        treframe = Frame(self, bg="#C6D9E3")
        treframe.pack(fill=BOTH, expand=True, padx=10, pady=5)

        Scrol_y = Scrollbar(treframe, orient=VERTICAL)
        Scrol_y.pack(side=RIGHT, fill=Y)

        Scrol_x = Scrollbar(treframe, orient=HORIZONTAL)
        Scrol_x.pack(side=BOTTOM, fill=X)

        tree_facturas = ttk.Treeview(treframe, columns=("Factura", "Cliente", "Precio", "Subtotal", 'Fecha'),
                                     show="headings", yscrollcommand=Scrol_y.set, xscrollcommand=Scrol_x.set)

        self.tree_ventas = tree_facturas
        Scrol_y.config(command=tree_facturas.yview)
        Scrol_x.config(command=tree_facturas.xview)

        tree_facturas.heading("#1", text="Factura")
        tree_facturas.heading("#2", text="Cliente")
        tree_facturas.heading("#3", text="Precio")
        tree_facturas.heading("#4", text="Subtotal")
        tree_facturas.heading("#5", text="Fecha")

        tree_facturas.column("Factura", width=100, anchor="center")
        tree_facturas.column("Cliente", width=200, anchor="center")
        tree_facturas.column("Precio", width=130, anchor="center")
        tree_facturas.column("Subtotal", width=130, anchor="center")
        tree_facturas.column("Fecha", width=130, anchor="center")

        tree_facturas.pack(fill=BOTH, expand=True)

        tree_facturas.bind('<<TreeviewSelect>>', self.on_venta_seleccion)
        self.refrescar_ventas()

    def buscar_venta(self, event=None):
        termino_cliente = self.entry_buscar_cliente.get().lower()
        termino_fecha = self.entry_buscar_fecha.get().lower()
        termino_factura = self.entry_buscar_factura.get().lower()
        self.refrescar_ventas(termino_cliente, termino_fecha, termino_factura)    

    def refrescar_ventas(self, termino_cliente="", termino_fecha="", termino_factura=""):
        ventas = self.mercadeo_service.listar_ventas()
        self.ventas_registradas = ventas  # Guardamos todas las ventas

        self.tree_ventas.delete(*self.tree_ventas.get_children())

        for venta in self.ventas_registradas:
            cliente = ClienteAR.get_by_id(venta.cliente_id)
            cliente_nombre = cliente.nombre.lower()
            fecha_venta = str(venta.fecha).lower()  # Convertir la fecha a string antes de usar lower()
            numero_factura = str(venta.numero_factura).lower()

            if (termino_cliente in cliente_nombre and
                    termino_fecha in fecha_venta and
                    termino_factura in numero_factura):
                self.tree_ventas.insert("", 0, text=venta.venta_id, values=(
                    venta.numero_factura, cliente.nombre, venta.total_neto, venta.total_pagado,
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
