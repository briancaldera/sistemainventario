import os
import sqlite3
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk, Frame, Label, Scrollbar, VERTICAL, HORIZONTAL, BOTH, X, Y, LEFT, RIGHT, BOTTOM

from model.producto import Producto
from services.ProductoService import ProductoService
from utils.fs_util import get_resource_path
from PIL import Image, ImageTk


class Inventario(tk.Frame):
    _colores_existencias: dict[str, str] = {
        'agotado': '#fc035a',
        'escaso': '#fcbe03',
        'disponible': '#03fc88',
    }

    def __init__(self, parent, controller):
        super().__init__(parent)
        self._producto_service = ProductoService()
        self.controller = controller
        self.producto_seleccionado: Producto | None = None
        self.productos: list[Producto] = []
        self.pack()
        self.widgets()
        self.actualizar_inventario()

    def widgets(self):

        frame1 = tk.Frame(self, bg="#dddddd", highlightbackground="gray", highlightthickness=1)
        frame1.pack()
        frame1.place(x=0, y=0, width=1100, height=100)

        titulo = tk.Label(self, text="INVENTARIOS", font=("Arial", 20), bg="#dddddd", anchor="center")
        titulo.pack()
        titulo.place(x=5, y=0, width=1090, height=90)

        frame2 = tk.Frame(self, bg="#C6D9E3", highlightbackground="gray", highlightthickness=1)
        frame2.place(x=0, y=100, width=1100, height=550)

        Labelframe = LabelFrame(frame2, text="productos", font=("Arial", 12), bg="#C6D9E3", fg="black")
        Labelframe.place(x=20, y=30, width=400, height=500)

        lblnombre = Label(Labelframe, text="Nombre: ", font=("Arial", 12), bg="#C6D9E3", fg="black")
        lblnombre.place(x=10, y=20)
        self.nombre = ttk.Entry(Labelframe, font=("Arial", 12))
        self.nombre.place(x=140, y=20, width=240, height=40)

        lblprecio = Label(Labelframe, text="Precio: ", font=("Arial", 12), bg="#C6D9E3", fg="black")
        lblprecio.place(x=10, y=80)
        self.precio = ttk.Entry(Labelframe, font=("Arial", 12))
        self.precio.place(x=140, y=80, width=240, height=40)

        lblcosto = Label(Labelframe, text="Costo: ", font=("Arial", 12), bg="#C6D9E3", fg="black")
        lblcosto.place(x=10, y=140)
        self.costo = ttk.Entry(Labelframe, font=("Arial", 12))
        self.costo.place(x=140, y=140, width=240, height=40)

        lblstock = Label(Labelframe, text="existencias: ", font=("Arial", 12), bg="#C6D9E3", fg="black")
        lblstock.place(x=10, y=200)
        self.stock = ttk.Entry(Labelframe, font=("Arial", 12))
        self.stock.place(x=140, y=200, width=240, height=40)

        boton_agregar = Button(Labelframe, text="Agregar", font=("Arial", 12), bg="gray", fg="white",
                               command=self.registrar)
        boton_agregar.place(x=80, y=340, width=240, height=40)

        boton_editar = Button(Labelframe, text="Editar", font=("Arial", 12), bg="gray", fg="white",
                              command=self.editar_producto)
        boton_editar.place(x=80, y=400, width=240, height=40)

        boton_reporte = Button(Labelframe, text="Reporte de Inventario", font=("Arial", 12), bg="gray", fg="white",
                               command=lambda: InventarioReporteScreen(self))
        boton_reporte.place(x=80, y=280, width=240, height=40)

        # tabla
        treFrame = Frame(frame2, bg="white")
        treFrame.place(x=450, y=30, width=630, height=400)

        scrol_y = ttk.Scrollbar(treFrame)
        scrol_y.pack(side=RIGHT, fill=Y)

        scrol_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill=X)

        self.tre = ttk.Treeview(treFrame, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set, height=40,
                                columns=("ID", "PRODUCTO", "PRECIO", "COSTO", "EXISTENCIAS"), show="headings")
        self.tre.pack(fill=BOTH, expand=True)

        scrol_y.config(command=self.tre.yview)
        scrol_x.config(command=self.tre.xview)

        self.tre.bind('<<TreeviewSelect>>', func=self.on_producto_seleccionado)

        self.tre.heading("ID", text="id")
        self.tre.heading("PRODUCTO", text="Producto")
        self.tre.heading("PRECIO", text="Precio")
        self.tre.heading("COSTO", text="Costo")
        self.tre.heading("EXISTENCIAS", text="Existencias")

        self.tre.column("ID", width=70, anchor="center")
        self.tre.column("PRODUCTO", width=150, anchor="center")
        self.tre.column("PRECIO", width=100, anchor="center")
        self.tre.column("COSTO", width=100, anchor="center")
        self.tre.column("EXISTENCIAS", width=100, anchor="center")

        for estado, color in self._colores_existencias.items():
            self.tre.tag_configure(estado, background=color)

        btn_actualizar = Button(frame2, text="Actualizar inventario", font=("Arial", 12), bg="gray", fg="white",
                                command=self.actualizar_inventario)
        btn_actualizar.place(x=440, y=480, width=260, height=50)

    def on_producto_seleccionado(self, event):
        selection = self.tre.selection()

        if len(selection) == 0:
            return

        for producto in self._productos:
            if producto.producto_id == int(selection[0]):
                self.producto_seleccionado = producto
                break

        self.limpiar_campos()
        self.nombre.insert(0, self.producto_seleccionado.nombre)
        self.precio.insert(0, self.producto_seleccionado.precio)
        self.costo.insert(0, self.producto_seleccionado.costo)
        self.stock.insert(0, self.producto_seleccionado.existencia)

    def validacion(self, nombre, precio, costo, existencia):
        if not (nombre and precio and costo and existencia):
            messagebox.showerror("Error", "Todos los campos son requeridos")
            return False
        try:
            float(precio)
            float(costo)
            int(existencia)
        except ValueError:
            messagebox.showerror("Error", "Precio, costo y existencias deben ser numeros")
            return False
        return True

    def actualizar_inventario(self):

        self.tre.delete(*self.tre.get_children())

        productos = self._producto_service.listar()

        self._productos = productos

        for producto in productos:
            if producto.existencia > 8:
                estado = 'disponible'
            elif producto.existencia > 0:
                estado = 'escaso'
            else:
                estado = 'agotado'

            self.tre.insert("", 0, iid=producto.producto_id, text=producto.producto_id,
                            values=(producto.producto_id, producto.nombre, producto.precio, producto.costo,
                                    producto.existencia), tags=(estado,))

    def registrar(self):
        nombre = self.nombre.get()
        precio = self.precio.get()
        costo = self.costo.get()
        existencia = self.stock.get()

        if self.validacion(nombre, precio, costo, existencia):
            try:

                request = self._producto_service.CrearProductoRequest(nombre, costo, precio, int(existencia))
                self._producto_service.crear(request)
                self.actualizar_inventario()
                self.limpiar_campos()
                messagebox.showinfo("Éxito", "Producto registrado correctamente")
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error al registrar el producto: {e}")
        else:
            messagebox.showerror("Error", "Error al registrar el producto")

    def editar_producto(self):
        if not self.producto_seleccionado:
            messagebox.showwarning("Editar producto", "Seleccione un producto")
            return

        item_id = self.producto_seleccionado.producto_id

        ventana_editar = Toplevel(self)
        ventana_editar.title("Editar producto")
        ventana_editar.geometry("400x400")
        ventana_editar.config(bg="#C6D9E3")

        lbl_nombre = Label(ventana_editar, text="Nombre: ", font=("Arial", 12), bg="#C6D9E3", fg="black")
        lbl_nombre.grid(row=0, column=0, padx=10, pady=10)
        entry_nombre = Entry(ventana_editar, font=("Arial", 12))
        entry_nombre.grid(row=0, column=1, padx=10, pady=10)
        entry_nombre.insert(0, self.producto_seleccionado.nombre)

        lbl_precio = Label(ventana_editar, text="Precio: ", font=("Arial", 12), bg="#C6D9E3", fg="black")
        lbl_precio.grid(row=2, column=0, padx=10, pady=10)
        entry_precio = Entry(ventana_editar, font=("Arial", 12))
        entry_precio.grid(row=2, column=1, padx=10, pady=10)
        entry_precio.insert(0, self.producto_seleccionado.precio)

        lbl_costo = Label(ventana_editar, text="Costo: ", font=("Arial", 12), bg="#C6D9E3", fg="black")
        lbl_costo.grid(row=3, column=0, padx=10, pady=10)
        entry_costo = Entry(ventana_editar, font=("Arial", 12))
        entry_costo.grid(row=3, column=1, padx=10, pady=10)
        entry_costo.insert(0, self.producto_seleccionado.costo)

        lbl_existencias = Label(ventana_editar, text="Existencias: ", font=("Arial", 12), bg="#C6D9E3", fg="black")
        lbl_existencias.grid(row=4, column=0, padx=10, pady=10)
        entry_existencias = Entry(ventana_editar, font=("Arial", 12))
        entry_existencias.grid(row=4, column=1, padx=10, pady=10)
        entry_existencias.insert(0, self.producto_seleccionado.existencia)

        def guardar_cambios():
            nombre = entry_nombre.get()
            precio = entry_precio.get()
            costo = entry_costo.get()
            existencias = entry_existencias.get()

            if not (nombre and precio and costo and existencias):
                messagebox.showerror("Error", "Todos los campos son requeridos")
                return

            try:
                precio = float(precio.replace(",", ""))
                costo = float(costo.replace(",", ""))
            except ValueError:
                messagebox.showerror("Error", "Precio y costo deben ser números")
                return

            request = ProductoService.ActualizarProductoRequest(id=item_id, nombre=nombre, costo=str(costo),
                                                                precio=str(precio), existencia=int(existencias))

            try:
                self._producto_service.actualizar(request)
                messagebox.showinfo('Cambios guardados', 'Los cambios fueron guardados')
            except Exception as e:
                print(e)
                messagebox.showerror('Error', 'Ocurrió un error al intentar actualizar el producto')

            self.actualizar_inventario()
            ventana_editar.destroy()

        btn_guardar = Button(ventana_editar, text="Guardar cambios", font=("Arial", 12), bg="gray", fg="white",
                             command=guardar_cambios)
        btn_guardar.place(x=80, y=250, width=240, height=40)

    def limpiar_campos(self):
        self.nombre.delete(0, tk.END)
        self.precio.delete(0, tk.END)
        self.costo.delete(0, tk.END)
        self.stock.delete(0, tk.END)


class InventarioReporteScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Reporte de Inventario")
        self.geometry("900x600")
        self.resizable(False, False)
        self.config(bg="#C6D9E3")

        self.producto_service = ProductoService()
        self.productos = []

        # Header
        images_folder = get_resource_path('imagenes')
        image_path = os.path.join(images_folder, "artvinil.png")

        header_frame = Frame(self, bg="#C6D9E3")
        header_frame.pack(fill='x')

        self.logo_image = Image.open(image_path)
        self.logo_image = self.logo_image.resize((150, 150))
        self.logo_image = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = Label(header_frame, image=self.logo_image, bg="#C6D9E3")
        self.logo_label.pack(pady=10)

        titulo_label = Label(header_frame, text="Reporte de Inventario", font=("Arial", 16), bg="#C6D9E3")
        titulo_label.pack(pady=10)

        # Search Fields
        frame_busqueda = Frame(self, bg="#C6D9E3")
        frame_busqueda.pack(fill=X, padx=10, pady=5)

        label_buscar_nombre = Label(frame_busqueda, text="Nombre:", bg="#C6D9E3", font=("Arial", 12))
        label_buscar_nombre.pack(side=LEFT, padx=5)
        self.entry_buscar_nombre = ttk.Entry(frame_busqueda, font=("Arial", 12))
        self.entry_buscar_nombre.pack(side=LEFT, padx=5)
        self.entry_buscar_nombre.bind("<KeyRelease>", self.buscar_productos)

        label_buscar_precio = Label(frame_busqueda, text="Precio:", bg="#C6D9E3", font=("Arial", 12))
        label_buscar_precio.pack(side=LEFT, padx=5)
        self.entry_buscar_precio = ttk.Entry(frame_busqueda, font=("Arial", 12))
        self.entry_buscar_precio.pack(side=LEFT, padx=5)
        self.entry_buscar_precio.bind("<KeyRelease>", self.buscar_productos)

        label_buscar_costo = Label(frame_busqueda, text="Costo:", bg="#C6D9E3", font=("Arial", 12))
        label_buscar_costo.pack(side=LEFT, padx=5)
        self.entry_buscar_costo = ttk.Entry(frame_busqueda, font=("Arial", 12))
        self.entry_buscar_costo.pack(side=LEFT, padx=5)
        self.entry_buscar_costo.bind("<KeyRelease>", self.buscar_productos)

        label_buscar_existencia = Label(frame_busqueda, text="Existencia:", bg="#C6D9E3", font=("Arial", 12))
        label_buscar_existencia.pack(side=LEFT, padx=5)
        self.entry_buscar_existencia = ttk.Entry(frame_busqueda, font=("Arial", 12))
        self.entry_buscar_existencia.pack(side=LEFT, padx=5)
        self.entry_buscar_existencia.bind("<KeyRelease>", self.buscar_productos)

        # Treeview
        treframe = Frame(self, bg="#C6D9E3")
        treframe.pack(fill=BOTH, expand=True, padx=10, pady=5)

        Scrol_y = Scrollbar(treframe, orient=VERTICAL)
        Scrol_y.pack(side=RIGHT, fill=Y)

        Scrol_x = Scrollbar(treframe, orient=HORIZONTAL)
        Scrol_x.pack(side=BOTTOM, fill=X)

        self.tree_productos = ttk.Treeview(
            treframe,
            columns=("Nombre", "Precio", "Costo", "Existencia"),
            show="headings",
            yscrollcommand=Scrol_y.set,
            xscrollcommand=Scrol_x.set
        )

        Scrol_y.config(command=self.tree_productos.yview)
        Scrol_x.config(command=self.tree_productos.xview)

        self.tree_productos.heading("#1", text="Nombre")
        self.tree_productos.heading("#2", text="Precio")
        self.tree_productos.heading("#3", text="Costo")
        self.tree_productos.heading("#4", text="Existencia")

        self.tree_productos.column("Nombre", width=200, anchor="center")
        self.tree_productos.column("Precio", width=100, anchor="center")
        self.tree_productos.column("Costo", width=100, anchor="center")
        self.tree_productos.column("Existencia", width=100, anchor="center")

        self.tree_productos.pack(fill=BOTH, expand=True)

        self.refrescar_productos()

    def buscar_productos(self, event=None):
        termino_nombre = self.entry_buscar_nombre.get().lower()
        termino_precio = self.entry_buscar_precio.get().lower()
        termino_costo = self.entry_buscar_costo.get().lower()
        termino_existencia = self.entry_buscar_existencia.get().lower()
        self.refrescar_productos(termino_nombre, termino_precio, termino_costo, termino_existencia)

    def refrescar_productos(self, termino_nombre="", termino_precio="", termino_costo="", termino_existencia=""):
        self.productos = self.producto_service.listar()
        self.tree_productos.delete(*self.tree_productos.get_children())

        for producto in self.productos:
            nombre = producto.nombre.lower()
            precio = str(producto.precio).lower()
            costo = str(producto.costo).lower()
            existencia = str(producto.existencia).lower()

            if (termino_nombre in nombre and
                    termino_precio in precio and
                    termino_costo in costo and
                    termino_existencia in existencia):
                self.tree_productos.insert(
                    "",
                    "end",
                    values=(producto.nombre, producto.precio, producto.costo, producto.existencia)
                )
