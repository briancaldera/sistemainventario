import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox

class Ventas(tk.Frame):

    db_name = "database.db"

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.numero_factura_actual = self.obtener_numero_factura_actual()
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

        self.entry_numero_factura = ttk.Entry(Lblframe, textvariable=self.numero_factura, state="readonly", font=("Arial", 12))
        self.entry_numero_factura.place(x=100, y=5, width=80)

        label_nombre = tk.Label(Lblframe, text="productos: ", font=("Arial", 12), bg="#C6D9E3", fg="black")
        label_nombre.place(x=200, y=12)

        self.entry_nombre = ttk.Combobox    (Lblframe, font=("Arial", 12), state="readonly")
        self.entry_nombre.place(x=280, y=10, width=180)
        self.cargar_productos()

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

        self.tree = ttk.Treeview(treframe, columns=("Producto", "Precio", "Cantidad", "subtotal"), show="headings", yscrollcommand=Scrol_y.set, xscrollcommand=Scrol_x.set)
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

        boton_agregar = Button(lblframe1, text="Agregar articulo", font=("Arial", 12), bg="#f4b400", command=self.registrar)
        boton_agregar.place(x=50, y=10, width=240, height=50)

        boton_pagar = Button(lblframe1, text="Pagar", font=("Arial", 12), bg="#f4b400", command=self.abrir_ventana_pago)
        boton_pagar.place(x=400, y=10, width=240, height=50)

        boton_facturas = Button(lblframe1, text="Ver Facturas", font=("Arial", 12), bg="#f4b400", command=self.abrir_ventana_factura)
        boton_facturas.place(x=750, y=10, width=240, height=50)

        self.label_suma_total = tk.Label(frame2, text="Total: ", font=("Arial", 12), bg="#C6D9E3")
        self.label_suma_total.place(x=360, y=335)

    def cargar_productos(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT nombre FROM inventario")
            productos = c.fetchall()
            self.entry_nombre["values"] = [producto[0] for producto in productos]
            if not productos:
                print("No hay productos en la base de datos")
                conn.close()
        except sqlite3.Error as e:
            print("error al cargar productos", e)     

    def actualizar_precio(self,event):
        nombre_producto = self.entry_nombre.get() 
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT precio FROM inventario WHERE nombre = ?", (nombre_producto,))
            precio = c.fetchone()
            if (precio):
                self.entry_valor.config(state="normal")
                self.entry_valor.delete(0, tk.END)
                self.entry_valor.insert(0, precio[0])
                self.entry_valor.config(state="readonly")
            else:
                self.entry_valor.config(state="normal")
                self.entry_valor.delete(0, tk.END)
                self.entry_valor.insert(0, "precio no disponible")
                self.entry_valor.config(state="readonly")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al obtener el precio: {e}")
        finally:
            conn.close()

    def actualizar_total(self):
        total = 0.0
        for child in self.tree.get_children():
            subtotal = float(self.tree.item(child, "values")[3])
            total += subtotal
        self.label_suma_total.config(text=f"Total: {total}") 

    def registrar(self):
        producto = self.entry_nombre.get()
        precio = self.entry_valor.get()
        cantidad = self.entry_cantidad.get()

        if producto and precio and cantidad: 
            try:
                cantidad = int(cantidad)
                if not self.verificar_existencias(producto, cantidad):
                    messagebox.showerror("Error", "No hay suficientes existencias")
                    return
                precio = float(precio)
                subtotal = precio * cantidad

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

    def verificar_existencias(self, nombre_producto, cantidad):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT existencia FROM inventario WHERE nombre = ?", (nombre_producto,))
            stock = c.fetchone()
            if stock and stock[0] >= cantidad:
                return True
            return False
        except sqlite3.Error as e:
            print("Error al verificar existencias", e)
            return False
        finally:
            conn.close()

    def obtener_total(self):
        total = 0.0
        for child in self.tree.get_children():
            subtotal = float(self.tree.item(child, "values")[3])
            total += subtotal
        return total
    
    def abrir_ventana_pago(self):
        if not self.tree.get_children():
            messagebox.showerror("Error", "No hay productos para pagar")
            return
        
        total = self.obtener_total()
        ventana_pago = tk.Toplevel(self)
        ventana_pago.title("Realizar Pago")
        ventana_pago.geometry("400x400")
        ventana_pago.resizable(False, False)
        ventana_pago.config(bg="#C6D9E3")

        label_total = tk.Label(ventana_pago, text=f"Total a pagar: {self.obtener_total()}", font=("Arial", 12), bg="#C6D9E3")
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

        boton_calcular = tk.Button(ventana_pago, text="Calcular Cambio", font=("Arial", 12), bg="white", command=calcular_cambio)
        boton_calcular.place(x=100, y=240, width=240, height=40)

        boton_pagar = tk.Button(ventana_pago, text="Pagar", font=("Arial", 12), bg="white", command=lambda: self.pagar(ventana_pago, entry_cantidad_pagada, label_cambio))
        boton_pagar.place(x=100, y=300, width=240, height=40)

    def pagar(self, ventana_pago, entry_cantidad_pagada, label_cambio):
        try:
            cantidad_pagada = float(entry_cantidad_pagada.get())
            total = self.obtener_total()
            cambio = cantidad_pagada - total
            if cambio < 0:
                messagebox.showerror("Error", "La cantidad pagada es insuficiente")
                return
            
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            try:
                for child in self.tree.get_children():
                    item = self.tree.item(child, "values")
                    nombre_producto = item[0]
                    cantidad_vendida = int(item[2])
                    if not self.verificar_existencias(nombre_producto, cantidad_vendida):
                        messagebox.showerror("Error", "No hay suficientes existencias: {nombre_producto}")
                        return
                    
                    c.execute("INSERT  INTO ventas (factura, nombre_articulo, valor_articulo, cantidad, subtotal) VALUES (?, ?, ?, ?, ?)", 
                              (self.numero_factura_actual, nombre_producto, float(item[1]), cantidad_vendida, float(item[3])))
                    c.execute("UPDATE inventario SET existencia = existencia - ? WHERE nombre = ?", (cantidad_vendida, nombre_producto))
                conn.commit()
                messagebox.showinfo("Venta", "Venta realizada con exito")

                self.numero_factura_actual += 1
                self.mostrar_numero_factura()

                for child in self.tree.get_children():
                    self.tree.delete(child)
                self.label_suma_total.config(text="Total: 0.0")

                ventana_pago.destroy()
            except sqlite3.Error as e:
                conn.rollback()
                messagebox.showerror("Error", f"Error al realizar la venta: {e}")
        except ValueError:
            messagebox.showerror("Error", "Cantidad no valida")

    def obtener_numero_factura_actual(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        try :
            c.execute("SELECT MAX(factura) FROM ventas")
            max_factura = c.fetchone()[0]
            if max_factura :
                return max_factura + 1
            else:
                return 1
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al obtener el número de factura: {e}")
            return 1
        finally:
            conn.close()

    def mostrar_numero_factura(self):  
        self.numero_factura.set(self.numero_factura_actual) 

    def abrir_ventana_factura(self):
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

        tree_facturas = ttk.Treeview(treframe, columns=("ID", "Factura", "Producto", "Precio", "cantidad", "Subtotal"), show="headings", yscrollcommand=Scrol_y.set, xscrollcommand=Scrol_x.set)
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

