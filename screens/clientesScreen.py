import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

from model.cliente import Cliente
from services.ClienteService import ClienteService


class ClientesScreen(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self._cliente_service = ClienteService()
        self._clientes = self._cliente_service.get_all_clientes()
        self._cliente_seleccionado = None
        self.widgets()
        self.actualizar_clientes()

    def widgets(self):
        # Frame para el título
        frame1 = tk.Frame(self, bg="#dddddd", highlightbackground="gray", highlightthickness=1)
        frame1.pack()
        frame1.place(x=0, y=0, width=1100, height=100)

        titulo = tk.Label(self, text="CLIENTES", font=("Arial", 20), bg="#dddddd", anchor="center")
        titulo.pack()
        titulo.place(x=5, y=0, width=1090, height=90)

        # Frame para el contenido principal
        frame2 = tk.Frame(self, bg="#C6D9E3", highlightbackground="gray", highlightthickness=1)
        frame2.place(x=0, y=100, width=1100, height=550)

        # LabelFrame para el formulario de cliente
        lblframe_cliente = tk.LabelFrame(frame2, text="Datos del cliente", font=("Arial", 12), bg="#C6D9E3", fg="black")
        lblframe_cliente.place(x=20, y=30, width=400, height=500)

        # Campos del formulario
        tk.Label(lblframe_cliente, text="Cédula:", font=("Arial", 12), bg="#C6D9E3").place(x=10, y=10)

        self.id_entry = ttk.Entry(lblframe_cliente, font=("Arial", 12))

        self.cedula_entry = ttk.Entry(lblframe_cliente, font=("Arial", 12))
        self.cedula_entry.place(x=140, y=10, width=240, height=40)

        tk.Label(lblframe_cliente, text="Nombre:", font=("Arial", 12), bg="#C6D9E3").place(x=10, y=70)
        self.nombre_entry = ttk.Entry(lblframe_cliente, font=("Arial", 12))
        self.nombre_entry.place(x=140, y=70, width=240, height=40)

        tk.Label(lblframe_cliente, text="Teléfono:", font=("Arial", 12), bg="#C6D9E3").place(x=10, y=130)
        self.telefono_entry = ttk.Entry(lblframe_cliente, font=("Arial", 12))
        self.telefono_entry.place(x=140, y=130, width=240, height=40)

        tk.Label(lblframe_cliente, text="Dirección:", font=("Arial", 12), bg="#C6D9E3").place(x=10, y=190)
        self.direccion_entry = ttk.Entry(lblframe_cliente, font=("Arial", 12))
        self.direccion_entry.place(x=140, y=190, width=240, height=40)

        # Botones del formulario
        ttk.Button(lblframe_cliente, text="Agregar", command=self.agregar_cliente).place(x=80, y=250, width=240,
                                                                                         height=40)
        ttk.Button(lblframe_cliente, text="Editar", command=self.editar_cliente).place(x=80, y=310, width=240,
                                                                                       height=40)
        # ttk.Button(lblframe_cliente, text="Eliminar", command=self.eliminar_cliente).place(x=80, y=370, width=240,
        #                                                                                    height=40)

        # Treeview para la tabla de clientes
        treframe = tk.Frame(frame2, bg="white")
        treframe.place(x=450, y=30, width=630, height=400)

        Scrol_y = ttk.Scrollbar(treframe)
        Scrol_y.pack(side=tk.RIGHT, fill=tk.Y)

        Scrol_x = ttk.Scrollbar(treframe, orient=tk.HORIZONTAL)
        Scrol_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.tree = ttk.Treeview(treframe, columns=("Cédula", "Nombre", "Telefono", "Direccion"), show="headings",
                                 yscrollcommand=Scrol_y.set, xscrollcommand=Scrol_x.set, selectmode='browse')
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', func=self.on_cliente_selected)

        Scrol_y.config(command=self.tree.yview)
        Scrol_x.config(command=self.tree.xview)

        self.tree.heading("#1", text="Cédula")
        self.tree.heading("#2", text="Nombre")
        self.tree.heading("#3", text="Teléfono")
        self.tree.heading("#4", text="Dirección")

        self.tree.column("Cédula", anchor="center")
        self.tree.column("Nombre", anchor="center")
        self.tree.column("Telefono", anchor="center")
        self.tree.column("Direccion", anchor="center")

        # Botón para actualizar la tabla
        btn_actualizar = ttk.Button(frame2, text="Actualizar Clientes", command=self.actualizar_clientes)
        btn_actualizar.place(x=440, y=480, width=260, height=50)

    def agregar_cliente(self):
        # Implementar la lógica para agregar un cliente
        cedula = self.cedula_entry.get()
        nombre = self.nombre_entry.get()
        telefono = self.telefono_entry.get()
        direccion = self.direccion_entry.get()

        try:
            self._cliente_service.save(cedula, nombre, telefono, direccion)
            self.limpiar_campos()
            self.actualizar_clientes()

            tk.messagebox.showinfo('Cliente registrado', 'Cliente registrado exitosamente')

        except Exception as e:
            print(e)
            tk.messagebox.showerror('Error', 'Ocurrió un error al intentar guardar al cliente')

    def editar_cliente(self):

        if self._cliente_seleccionado is None:
            return

        cliente_id = self._cliente_seleccionado.id
        cedula = self.cedula_entry.get()
        nombre = self.nombre_entry.get()
        telefono = self.telefono_entry.get()
        direccion = self.direccion_entry.get()

        data = {
            'cedula': cedula,
            'nombre': nombre,
            'telefono': telefono,
            'direccion': direccion
        }

        try:
            self._cliente_service.update_cliente(cliente_id, data)
            self.limpiar_campos()
            self.actualizar_clientes()

            tk.messagebox.showinfo('Cliente actualizado', 'Cliente actualizado exitosamente')

        except Exception as e:
            print(e)
            tk.messagebox.showerror('Error', 'Ocurrió un error al intentar actualizar al cliente')

    def eliminar_cliente(self):
        # todo remove this
        return
        id = self.id_entry.get()

        try:
            self._cliente_service.delete_cliente(int(id))
            self.limpiar_campos()
            self.actualizar_clientes()

            tk.messagebox.showinfo('Cliente eliminado', 'Cliente eliminado exitosamente')

        except Exception as e:
            print(e)
            tk.messagebox.showerror('Error', 'Ocurrió un error al intentar eliminar al cliente')

    def actualizar_clientes(self):
        # Implementar la lógica para actualizar la tabla de clientes
        clientes = self._cliente_service.get_all_clientes()

        self._clientes = clientes

        self.tree.delete(*self.tree.get_children())

        for cliente in clientes:
            self.tree.insert('', tk.END, values=(cliente.cedula, cliente.nombre, cliente.telefono, cliente.direccion),
                             iid=cliente.id)

        self._cliente_seleccionado = None

    def on_cliente_selected(self, event) -> None:
        selection = self.tree.selection()

        if len(selection) == 0:
            return

        item_id = selection[0]

        for cliente in self._clientes:
            if cliente.id == int(item_id):
                self._cliente_seleccionado = cliente
                break

        cliente_seleccionado = self._cliente_seleccionado

        self.id_entry.delete(0, tk.END)
        self.id_entry.insert(0, cliente_seleccionado.id)

        self.cedula_entry.delete(0, tk.END)
        self.cedula_entry.insert(0, cliente_seleccionado.cedula)

        self.nombre_entry.delete(0, tk.END)
        self.nombre_entry.insert(0, cliente_seleccionado.nombre)

        self.telefono_entry.delete(0, tk.END)
        self.telefono_entry.insert(0, cliente_seleccionado.telefono)

        self.direccion_entry.delete(0, tk.END)
        self.direccion_entry.insert(0, cliente_seleccionado.direccion)

    def limpiar_campos(self):
        self.id_entry.delete(0, tk.END)
        self.cedula_entry.delete(0, tk.END)
        self.nombre_entry.delete(0, tk.END)
        self.telefono_entry.delete(0, tk.END)
        self.direccion_entry.delete(0, tk.END)
