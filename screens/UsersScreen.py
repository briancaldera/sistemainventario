import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from screens.RegisterScreen import RegisterScreen


class UsersScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, background='#E0F2F7')
        self.controller = controller
        self._widgets()
        self.load_table()

    def _widgets(self):

        frame2 = tk.Frame(self, bg="#C6D9E3", highlightbackground="gray", highlightthickness=1)
        frame2.place(x=0, y=100, width=1100, height=550)

        titulo = tk.Label(self, text="USUARIOS", font=("Arial", 20), bg="#C6D9E3", anchor="center")
        titulo.pack()
        titulo.place(x=5, y=0, width=1090, height=90)

        usuarion_label = tk.Label(frame2, text='Nombre de usuario', bg="#C6D9E3", font=("Arial", 12))
        usuarion_label.place(x=100, y=150)


        self.username = tk.Entry(frame2, )
        self.username.place(x=100, y=200)

        fecha_registro_label = tk.Label(frame2, text='Fecha de registro', bg="#C6D9E3", font=("Arial", 12))
        fecha_registro_label.place(x=100, y=250)

        self.fecha_registro = tk.Entry(frame2, )
        self.fecha_registro.place(x=100, y=300)

        rol_label = tk.Label(frame2, text='Rol del usuario', bg="#C6D9E3", font=("Arial", 12))
        rol_label.place(x=100, y=350)

        self.rol_var = tk.StringVar()
        self.rol = tk.ttk.Combobox(frame2, values=('vendedor', 'admin'), textvariable=self.rol_var)
        self.rol.bind('<<ComboboxSelected>>', self.change_user_role)


        self.rol.place(x=100, y=400)

        # Treeview para la tabla de clientes
        treframe = tk.Frame(frame2, bg="white")
        treframe.place(x=450, y=30, width=630, height=400)

        Scrol_y = ttk.Scrollbar(treframe)
        Scrol_y.pack(side=tk.RIGHT, fill=tk.Y)

        Scrol_x = ttk.Scrollbar(treframe, orient=tk.HORIZONTAL)
        Scrol_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.tree = ttk.Treeview(treframe, columns=("Nombre de usuario", "Fecha de registro", 'Rol'), show="headings",
                                 yscrollcommand=Scrol_y.set, xscrollcommand=Scrol_x.set, selectmode='browse')
        self.tree.bind('<<TreeviewSelect>>', func=self.on_user_selected)
        self.tree.pack(fill=tk.BOTH, expand=True)

        Scrol_y.config(command=self.tree.yview)
        Scrol_x.config(command=self.tree.xview)

        self.tree.heading("#1", text="Nombre de usuario")
        self.tree.heading("#2", text="Fecha de registro")
        self.tree.heading("#3", text="Rol")

        self.tree.column("Nombre de usuario", anchor="center")
        self.tree.column("Fecha de registro", anchor="center")
        self.tree.column("Rol", anchor="center")

        self.register_user_button = tk.Button(self, text='Registrar usuario', command=self.show_register_user_screen)
        self.register_user_button.place(x=200, y=600)

    def show_register_user_screen(self):
        register_user_screen = RegisterScreen()
        register_user_screen.mainloop()

    def change_user_role(self, event):
        username = self.username.get()
        new_role = self.rol.get()

        res = self.controller.update_role(username, new_role)

        if res:
            messagebox.showinfo('Rol cambiado', f'El rol del usuario fue cambiado exitosamente a [{new_role}]')
            self.load_table()
        else:
            messagebox.showerror('Error', 'Ocurrió un error al intentar cambiar el rol del usuario')

    def on_user_selected(self, event) -> None:
        selection = self.tree.selection()

        if len(selection) == 0:
            return

        id = selection[0]
        item = self.tree.item(id)

        username = item["values"][0]
        registered_at = item["values"][1]
        rol = item["values"][2]

        self.username.delete(0, tk.END)
        self.username.insert(0, username)

        self.fecha_registro.delete(0, tk.END)
        self.fecha_registro.insert(0, registered_at)

        self.rol.set(rol)

        pass

    def load_table(self):
        users = self.controller.load_users()

        for row in self.tree.get_children():
            self.tree.delete(row)

        for user in users:
            self.tree.insert('', tk.END, values=(user.name.name, user.created_at, user.rol))
