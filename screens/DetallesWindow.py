import tkinter as tk
from tkinter import ttk

from model.cliente import ClienteAR
from model.compra import Compra, Ingreso
from model.producto import Producto
from model.proveedor import ProveedorAR
from model.referencia import Referencia
from model.venta import Venta, Egreso


class DetallesWindow(tk.Toplevel):
    def __init__(self, parent, operacion: Venta | Compra):
        super().__init__(parent)

        self.operacion = operacion
        self.referencia = Referencia.get_by_id(operacion.referencia_id)

        if isinstance(operacion, Compra):
            self.sujeto = ProveedorAR.get_by_id(operacion.proveedor_id)
        else:
            self.sujeto = ClienteAR.get_by_id(operacion.cliente_id)

        self.productos_con_cantidad = []

        self.title(
            f'Venta Nro. {operacion.numero_factura}' if isinstance(operacion, Venta) else f'Compra Nro. {operacion.numero_compra}')
        self.resizable(width=False, height=True)
        self.geometry('1000x700+10+20')

        self.productos_tabla = None
        self.widgets()

        self.detallado = None
        if isinstance(operacion, Compra):
            self.detallado = Ingreso.select().where(Ingreso.compra_id == operacion.compra_id)
        else:
            self.detallado = Egreso.select().where(Egreso.venta_id == operacion.venta_id)

        for detalle in self.detallado:
            producto = Producto.get_by_id(detalle.producto_id)
            self.productos_con_cantidad.append({'producto': producto, 'cantidad': detalle.cantidad})

        assert self.productos_tabla is not None

        self.productos_tabla.delete(*self.productos_tabla.get_children())
        for producto in self.productos_con_cantidad:
            if isinstance(operacion, Compra):
                self.productos_tabla.insert("", "end", values=(
                    producto["producto"].nombre, producto["producto"].costo, producto['producto'].costo * self.referencia.valor, producto["cantidad"],
                    producto["producto"].costo * producto["cantidad"]))
            else:
                self.productos_tabla.insert("", "end", values=(
                    producto["producto"].nombre, producto["producto"].precio, producto['producto'].precio * self.referencia.valor, producto["cantidad"],
                    producto["producto"].precio * producto["cantidad"]))

    def widgets(self):
        frame1 = tk.Frame(self, bg="#C6D9E3", highlightbackground="gray", highlightthickness=1)
        frame1.pack(fill=tk.BOTH, expand=True)

        nombre_sujeto = tk.Label(frame1, text=f"Cliente: {self.sujeto.nombre}")
        nombre_sujeto.place(x=10, y=10)

        if isinstance(self.operacion, Venta):
            cedula_sujeto = tk.Label(frame1, text=f"Cedula: {self.sujeto.cedula}")
            cedula_sujeto.place(x=10, y=40)

        direccion_sujeto = tk.Label(frame1, text=f"Dirección: {self.sujeto.direccion}")
        direccion_sujeto.place(x=10, y=70)

        telefono_sujeto = tk.Label(frame1, text=f"Teléfono: {self.sujeto.telefono}")
        telefono_sujeto.place(x=10, y=100)

        numero_operacion = tk.Label(frame1, text=f"Nro. {'Orden de compra: ' if isinstance(self.operacion, Compra) else 'Factura: '}: {self.operacion.numero_compra if isinstance(self.operacion, Compra) else self.operacion.numero_factura}")
        numero_operacion.place(x=100, y=10)

        referencia = tk.Label(frame1, text=f"Referencia: Bs. {self.referencia.valor}")
        referencia.place(x=500, y=100)

        # Tabla de productos

        scroll_y = tk.Scrollbar(self, orient=tk.VERTICAL)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        scroll_x = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.productos_tabla = ttk.Treeview(self,
                                            columns=("Producto", "Precio", 'Precio en Bolívares', "Cantidad", "Total"),
                                            show="headings", yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.productos_tabla.pack(fill=tk.BOTH, expand=True)

        scroll_y.config(command=self.productos_tabla.yview)
        scroll_x.config(command=self.productos_tabla.xview)

        self.productos_tabla.heading("#1", text="Producto")
        self.productos_tabla.heading("#2", text="Precio" if isinstance(self.operacion, Venta) else "Costo")
        self.productos_tabla.heading("#3", text='Precio en Bolívares')
        self.productos_tabla.heading("#4", text="Cantidad")
        self.productos_tabla.heading("#5", text="Total")

        self.productos_tabla.column("#1", anchor="center")
        self.productos_tabla.column("#2", anchor="center")
        self.productos_tabla.column("#3", anchor="center")
        self.productos_tabla.column("#4", anchor="center")
        self.productos_tabla.column("#5", anchor="center")
