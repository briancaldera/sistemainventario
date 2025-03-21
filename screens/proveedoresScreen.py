import tkinter as tk
import tkinter.ttk as ttk

class ProveedoresScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.widgets()

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
        lblframe_proveedor = tk.LabelFrame(frame2, text="Datos del proveedor", font=("Arial", 12), bg="#C6D9E3", fg="black")
        lblframe_proveedor.place(x=20, y=30, width=400, height=500)

        # Campos del formulario
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
        ttk.Button(lblframe_proveedor, text="Agregar", command=self.agregar_proveedor).place(x=80, y=200, width=240, height=40)
        ttk.Button(lblframe_proveedor, text="Editar", command=self.editar_proveedor).place(x=80, y=260, width=240, height=40)
        ttk.Button(lblframe_proveedor, text="Eliminar", command=self.eliminar_proveedor).place(x=80, y=320, width=240, height=40)

        # Treeview para la tabla de proveedores
        treframe = tk.Frame(frame2, bg="white")
        treframe.place(x=450, y=30, width=630, height=400)

        Scrol_y = ttk.Scrollbar(treframe)
        Scrol_y.pack(side=tk.RIGHT, fill=tk.Y)

        Scrol_x = ttk.Scrollbar(treframe, orient=tk.HORIZONTAL)
        Scrol_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.tree = ttk.Treeview(treframe, columns=("Nombre", "Telefono", "Direccion"), show="headings", yscrollcommand=Scrol_y.set, xscrollcommand=Scrol_x.set)
        self.tree.pack(fill=tk.BOTH, expand=True)

        Scrol_y.config(command=self.tree.yview)
        Scrol_x.config(command=self.tree.xview)

        self.tree.heading("#1", text="Nombre")
        self.tree.heading("#2", text="Teléfono")
        self.tree.heading("#3", text="Dirección")

        self.tree.column("Nombre", anchor="center")
        self.tree.column("Telefono", anchor="center")
        self.tree.column("Direccion", anchor="center")

        # Botón para actualizar la tabla
        btn_actualizar = ttk.Button(frame2, text="Actualizar Proveedores", command=self.actualizar_proveedores)
        btn_actualizar.place(x=440, y=480, width=260, height=50)

    def agregar_proveedor(self):
        # Implementar la lógica para agregar un proveedor
        pass

    def editar_proveedor(self):
        # Implementar la lógica para editar un proveedor
        pass

    def eliminar_proveedor(self):
        # Implementar la lógica para eliminar un proveedor
        pass

    def actualizar_proveedores(self):
        # Implementar la lógica para actualizar la tabla de proveedores
        pass