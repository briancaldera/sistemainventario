import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox

class Inventario(tk.Frame):

    db_name = "database.db"

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.pack()
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.widgets()

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
        lblnombre.place(x=10, y=10)
        self.nombre = ttk.Entry(Labelframe, font=("Arial", 12))
        self.nombre.place(x=140, y=20, width=240, height=40)

        lblproveedor = Label(Labelframe, text="Proveedor: ", font=("Arial", 12), bg="#C6D9E3", fg="black")
        lblproveedor.place(x=10, y=80)
        self.proveedor = ttk.Entry(Labelframe, font=("Arial", 12))
        self.proveedor.place(x=140, y=80, width=240, height=40)

        lblprecio = Label(Labelframe, text="Precio: ", font=("Arial", 12), bg="#C6D9E3", fg="black")
        lblprecio.place(x=10, y=140)
        self.precio = ttk.Entry(Labelframe, font=("Arial", 12))
        self.precio.place(x=140, y=140, width=240, height=40)

        lblcosto = Label(Labelframe, text="Costo: ", font=("Arial", 12), bg="#C6D9E3", fg="black")
        lblcosto.place(x=10, y=200)
        self.costo = ttk.Entry(Labelframe, font=("Arial", 12))
        self.costo.place(x=140, y=200, width=240, height=40)

        lblstock = Label(Labelframe, text="existencias: ", font=("Arial", 12), bg="#C6D9E3", fg="black")
        lblstock.place(x=10, y=260)
        self.stock = ttk.Entry(Labelframe, font=("Arial", 12))
        self.stock.place(x=140, y=260, width=240, height=40)

        boton_agregar = Button(Labelframe, text="Agregar", font=("Arial", 12), bg="gray", fg="white", command=self.registrar)
        boton_agregar.place(x=80, y=340, width=240, height=40)

        boton_editar = Button(Labelframe, text="Editar", font=("Arial", 12), bg="gray", fg="white", command=self.editar_producto)
        boton_editar.place(x=80, y=400, width=240, height=40)


        #tabla
        treFrame = Frame(frame2, bg="white")
        treFrame.place(x=450, y=30, width=630, height=400)

        scrol_y = ttk.Scrollbar(treFrame)
        scrol_y.pack(side=RIGHT, fill=Y)

        scrol_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill=X)

        self.tre = ttk.Treeview(treFrame, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set, height=40,
                                 columns=("ID", "PRODUCTO", "PROVEEDOR", "PRECIO", "COSTO", "EXISTENCIAS"), show="headings")
        self.tre.pack(fill=BOTH, expand=True)

        scrol_y.config(command=self.tre.yview)
        scrol_x.config(command=self.tre.xview)

        self.tre.heading("ID", text="id")
        self.tre.heading("PRODUCTO", text="Producto")
        self.tre.heading("PROVEEDOR", text="Proveedor")
        self.tre.heading("PRECIO", text="Precio")
        self.tre.heading("COSTO", text="Costo")
        self.tre.heading("EXISTENCIAS", text="Existencias")

        self.tre.column("ID", width=70, anchor="center")
        self.tre.column("PRODUCTO", width=150, anchor="center")
        self.tre.column("PROVEEDOR", width=150, anchor="center")
        self.tre.column("PRECIO", width=100, anchor="center")
        self.tre.column("COSTO", width=100, anchor="center")
        self.tre.column("EXISTENCIAS", width=100, anchor="center")

        self.mostrar()

        btn_actualizar = Button(frame2, text="Actualizar inventario", font=("Arial", 12), bg="gray", fg="white", command=self.actualizar_inventario)
        btn_actualizar.place(x=440, y=480, width=260, height=50)

    def eje_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            resultado = cursor.execute(consulta, parametros)
            conn.commit()
        return resultado
    
    def validacion(self, nombre, proveedor, precio, costo, existencia):
        if not (nombre and proveedor and precio and costo and existencia):
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
    
    def mostrar(self):
        # Limpiar el Treeview
        for item in self.tre.get_children():
            self.tre.delete(item)

        consulta = "SELECT * FROM inventario ORDER BY producto_id DESC"
        resultado = self.eje_consulta(consulta)
        for elem in resultado:
            try:
                precio_d = "{:.2f}".format(float(elem[3])) if elem[3] else ""
                costo_d = "{:.2f}".format(float(elem[4])) if elem[4] else ""
            except ValueError:
                precio_d = elem[3]
                costo_d = elem[4]
                
            self.tre.insert("", 0, text=elem[0], values=(elem[0], elem[1], elem[2], precio_d, costo_d, elem[5]))

    def actualizar_inventario(self):
        for item in self.tre.get_children():
            self.tre.delete(item)

        self.mostrar()

        messagebox.showinfo("Inventario", "Inventario actualizado")  

    def registrar(self):
        nombre = self.nombre.get()
        prov = self.proveedor.get()
        precio = self.precio.get()
        costo = self.costo.get()
        existencia = self.stock.get()

        if self.validacion(nombre, prov, precio, costo, existencia):
            try:
                consulta = "INSERT INTO inventario VALUES(?, ?, ?, ?, ?, ?)"
                parametros = (None, nombre, prov, precio, costo, existencia)
                self.eje_consulta(consulta, parametros)
                self.mostrar() #se actualiza el treview aqui
                self.nombre.delete(0, END)
                self.proveedor.delete(0, END)
                self.precio.delete(0, END)
                self.costo.delete(0, END)
                self.stock.delete(0, END)
                messagebox.showinfo("Éxito", "Producto registrado correctamente")
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error al registrar el producto: {e}")
        else:
            messagebox.showerror("Error", "Error al registrar el producto")

    def editar_producto(self):
        seleccion = self.tre.selection()
        if not seleccion:
            messagebox.showwarning("Editar producto", "Seleccione un producto")
            return
    
        item_id = self.tre.item(seleccion)["text"]
        item_values = self.tre.item(seleccion)["values"]

        ventana_editar = Toplevel(self)
        ventana_editar.title("Editar producto")
        ventana_editar.geometry("400x400")
        ventana_editar.config(bg="#C6D9E3")

        lbl_nombre = Label(ventana_editar, text="Nombre: ", font=("Arial", 12), bg="#C6D9E3", fg="black")
        lbl_nombre.grid(row=0, column=0, padx=10, pady=10)
        entry_nombre = Entry(ventana_editar, font=("Arial", 12))
        entry_nombre.grid(row=0, column=1, padx=10, pady=10)
        entry_nombre.insert(0, item_values[1])

        lbl_proveedor = Label(ventana_editar, text="Proveedor: ", font=("Arial", 12), bg="#C6D9E3", fg="black")
        lbl_proveedor.grid(row=1, column=0, padx=10, pady=10)
        entry_proveedor = Entry(ventana_editar, font=("Arial", 12))
        entry_proveedor.grid(row=1, column=1, padx=10, pady=10)
        entry_proveedor.insert(0, item_values[2])

        lbl_precio = Label(ventana_editar, text="Precio: ", font=("Arial", 12), bg="#C6D9E3", fg="black")
        lbl_precio.grid(row=2, column=0, padx=10, pady=10)
        entry_precio = Entry(ventana_editar, font=("Arial", 12))
        entry_precio.grid(row=2, column=1, padx=10, pady=10)
        entry_precio.insert(0, item_values[3].split()[0].replace(",", ""))

        lbl_costo = Label(ventana_editar, text="Costo: ", font=("Arial", 12), bg="#C6D9E3", fg="black")
        lbl_costo.grid(row=3, column=0, padx=10, pady=10)
        entry_costo = Entry(ventana_editar, font=("Arial", 12))
        entry_costo.grid(row=3, column=1, padx=10, pady=10)
        entry_costo.insert(0, item_values[4].split()[0].replace(",", ""))

        lbl_existencias = Label(ventana_editar, text="Existencias: ", font=("Arial", 12), bg="#C6D9E3", fg="black")
        lbl_existencias.grid(row=4, column=0, padx=10, pady=10)
        entry_existencias = Entry(ventana_editar, font=("Arial", 12))
        entry_existencias.grid(row=4, column=1, padx=10, pady=10)
        entry_existencias.insert(0, item_values[5])

        def guardar_cambios():
            nombre = entry_nombre.get()
            proveedor = entry_proveedor.get()
            precio = entry_precio.get()
            costo = entry_costo.get()
            existencias = entry_existencias.get()

            if not (nombre and proveedor and precio and costo and existencias):
                messagebox.showerror("Error", "Todos los campos son requeridos")
                return
            
            try: 
                precio = float(precio.replace(",", ""))
                costo = float(costo.replace(",", ""))
            except ValueError:
                messagebox.showerror("Error", "Precio y costo deben ser números")
                return

            consulta = "UPDATE inventario SET nombre = ?, proveedor = ?, precio = ?, costo = ?, existencia = ? WHERE id = ?"
            parametros = (nombre, proveedor, precio, costo, existencias, item_id)
            self.eje_consulta(consulta, parametros)
            self.actualizar_inventario()
            ventana_editar.destroy()

        btn_guardar = Button(ventana_editar, text="Guardar cambios", font=("Arial", 12), bg="gray", fg="white", command=guardar_cambios)
        btn_guardar.place(x=80, y=250, width=240, height=40)        

