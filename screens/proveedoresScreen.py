
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from services.ProveedorServices import ProveedorService


class ProveedoresScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self._proveedores_service = ProveedorService()
        self.widgets()
        self.actualizar_proveedores()

    def widgets(self):
        # Frame para el título
        frame1 = tk.Frame(self, bg="#dddddd", highlightbackground="gray", highlightthickness=1)
        frame1.pack()
        frame1.place(x=0, y=0, width=1100, height=100)

        titulo = tk.Label(self, text="PROVEEDORES", font=("Arial", 20), bg="#dddddd", anchor="center")
        titulo.pack()
        titulo.place(x=5, y=0, width=1090, height=90)

        # Frame para el contenido principal
        frame2 = tk.Frame(self, bg="#C6D9E3", highlightbackground="gray", highlightthickness=1)
        frame2.place(x=0, y=100, width=1100, height=550)

        # LabelFrame para el formulario de proveedor
        lblframe_proveedor = tk.LabelFrame(frame2, text="Datos del proveedor", font=("Arial", 12), bg="#C6D9E3",
                                           fg="black")
        lblframe_proveedor.place(x=20, y=30, width=400, height=500)

        # Campos del formulario

        self.id_entry = ttk.Entry(lblframe_proveedor, font=("Arial", 12))

        tk.Label(lblframe_proveedor, text="Nombre:", font=("Arial", 12), bg="#C6D9E3").place(x=10, y=10)
        self.nombre_entry = ttk.Entry(lblframe_proveedor, font=("Arial", 12))
        self.nombre_entry.place(x=140, y=20, width=240, height=40)

        tk.Label(lblframe_proveedor, text="Teléfono:", font=("Arial", 12), bg="#C6D9E3").place(x=10, y=80)
        self.telefono_entry = ttk.Entry(lblframe_proveedor, font=("Arial", 12))
        self.telefono_entry.place(x=140, y=80, width=240, height=40)

        tk.Label(lblframe_proveedor, text="Dirección:", font=("Arial", 12), bg="#C6D9E3").place(x=10, y=140)
        self.direccion_entry = ttk.Entry(lblframe_proveedor, font=("Arial", 12))
        self.direccion_entry.place(x=140, y=140, width=240, height=40)

        # Botones del formulario
        ttk.Button(lblframe_proveedor, text="Agregar", command=self.agregar_proveedor).place(x=80, y=200, width=240,
                                                                                             height=40)
        ttk.Button(lblframe_proveedor, text="Editar", command=self.editar_proveedor).place(x=80, y=260, width=240,
                                                                                           height=40)
        # ttk.Button(lblframe_proveedor, text="Eliminar", command=self.eliminar_proveedor).place(x=80, y=320, width=240,
        #                                                                                        height=40)

        # Treeview para la tabla de proveedores
        treframe = tk.Frame(frame2, bg="white")
        treframe.place(x=450, y=30, width=630, height=400)

        Scrol_y = ttk.Scrollbar(treframe)
        Scrol_y.pack(side=tk.RIGHT, fill=tk.Y)

        Scrol_x = ttk.Scrollbar(treframe, orient=tk.HORIZONTAL)
        Scrol_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.tree = ttk.Treeview(treframe, columns=("ID", "Nombre", "Telefono", "Direccion"), show="headings",
                                 yscrollcommand=Scrol_y.set, xscrollcommand=Scrol_x.set, selectmode='browse')

        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', func=self.on_proveedor_selected)

        Scrol_y.config(command=self.tree.yview)
        Scrol_x.config(command=self.tree.xview)

        self.tree.heading("#1", text="ID")
        self.tree.heading("#2", text="Nombre")
        self.tree.heading("#3", text="Teléfono")
        self.tree.heading("#4", text="Dirección")

        self.tree.column("ID", anchor="center")
        self.tree.column("Nombre", anchor="center")
        self.tree.column("Telefono", anchor="center")
        self.tree.column("Direccion", anchor="center")

        # Botón para actualizar la tabla
        btn_actualizar = ttk.Button(frame2, text="Actualizar Proveedores", command=self.actualizar_proveedores)
        btn_actualizar.place(x=440, y=480, width=260, height=50)

    def agregar_proveedor(self):
        # Implementar la lógica para agregar un proveedor
        nombre = self.nombre_entry.get()
        telefono = self.telefono_entry.get()
        direccion = self.direccion_entry.get()

        try:
            self._proveedores_service.save(nombre, telefono, direccion)
            self.limpiar_campos()
            self.actualizar_proveedores()

            tk.messagebox.showinfo('Proveedor registrado', 'Proveedor registrado exitosamente')

        except Exception as e:
            print(e)
            tk.messagebox.showerror('Error', 'Ocurrió un error al intentar guardar al proveedor')

        pass

    def editar_proveedor(self):
        # Implementar la lógica para editar un proveedor

        id = self.id_entry.get()
        nombre = self.nombre_entry.get()
        telefono = self.telefono_entry.get()
        direccion = self.direccion_entry.get()

        data = {
            'nombre': nombre,
            'telefono': telefono,
            'direccion': direccion
        }

        try:

            self._proveedores_service.update_proveedor(int(id), data)
            self.limpiar_campos()
            self.actualizar_proveedores()

            tk.messagebox.showinfo('Proveedor actualizado', 'Proveedor actualizado exitosamente')

        except Exception as e:
            print(e)
            tk.messagebox.showerror('Error', 'Ocurrió un error al intentar actualizar al proveedor')

        pass

    def eliminar_proveedor(self):
        # Implementar la lógica para eliminar un proveedor

        id = self.id_entry.get()

        try:

            self._proveedores_service.delete_proveedor(int(id))
            self.limpiar_campos()
            self.actualizar_proveedores()

            tk.messagebox.showinfo('Proveedor eliminado', 'Proveedor eliminado exitosamente')

        except Exception as e:
            print(e)
            tk.messagebox.showerror('Error', 'Ocurrió un error al intentar eliminar al proveedor')

        pass

    def actualizar_proveedores(self):
        # Implementar la lógica para actualizar la tabla de proveedores
        proveedores = self._proveedores_service.get_all_proveedores()

        for row in self.tree.get_children():
            self.tree.delete(row)

        for proveedor in proveedores:
            self.tree.insert('', tk.END,
                             values=(proveedor.id, proveedor.nombre, proveedor.telefono, proveedor.direccion))
        pass

    def on_proveedor_selected(self, event) -> None:
        selection = self.tree.selection()

        if len(selection) == 0:
            return

        id = selection[0]
        item = self.tree.item(id)

        id = item["values"][0]
        nombre = item["values"][1]
        telefono = item["values"][2]
        direccion = item["values"][3]

        self.id_entry.delete(0, tk.END)
        self.id_entry.insert(0, id)

        self.nombre_entry.delete(0, tk.END)
        self.nombre_entry.insert(0, nombre)

        self.telefono_entry.delete(0, tk.END)
        self.telefono_entry.insert(0, telefono)

        self.direccion_entry.delete(0, tk.END)
        self.direccion_entry.insert(0, direccion)

    def limpiar_campos(self):
        self.id_entry.delete(0, tk.END)
        self.nombre_entry.delete(0, tk.END)
        self.telefono_entry.delete(0, tk.END)
        self.direccion_entry.delete(0, tk.END)