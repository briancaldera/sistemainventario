import tkinter as tk
from tkinter import messagebox


class RegisterScreen(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent, background='#6CD9E3')
        self.controller = controller
        self.widgets()


    def widgets(self):
        self.title_label = tk.Label(self, text='Registrar usuario')
        self.title_label.pack()
        self.username_label = tk.Label(self, text='Usuario:')
        self.username_label.pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        self.password_label = tk.Label(self, text='Contraseña:')
        self.password_label.pack()
        self.password_entry = tk.Entry(self)
        self.password_entry.pack()

        self.register_button = tk.Button(self, text='Registrar', command=self.register_user)
        self.register_button.pack()

        self.user_exists_button = tk.Button(self, text='Ya tengo usuario',
                                            command=lambda: self.controller.show_frame('LoginScreen'))
        self.user_exists_button.pack()

    def register_user(self):
        res = self.controller.register_user(self.username_entry.get(), self.password_entry.get())

        if res:
            messagebox.showinfo('Usuario registrado', 'El usuario ha sido registrado')
            self.controller.show_frame('LoginScreen')
        else:
            messagebox.showerror('Error', 'Ocurrió un error al registrar el usuario')