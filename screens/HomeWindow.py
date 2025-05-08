import tkinter as tk
from tkinter import messagebox

from auth.AuthManager import AuthManager
from screens.ManagerScreen import Manager
from screens.LoginScreen import LoginScreen


class HomeWindow(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('Sistema de inventario')
        self.resizable(False, False)
        self.geometry("400x400+120+20")

        self.auth = AuthManager.get_instance()

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in tuple([LoginScreen]):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky='nsew')

            self.show_frame('LoginScreen') # Mostrar LoginScreen al inicio

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def login_user(self, username: str, password: str) -> None:

        res = self.auth.login(username, password)

        if res:
            self.destroy()
            manager = Manager()
            manager.mainloop()
        else:
            messagebox.showwarning('Credenciales incorrectas', 'El usuario o la contraseña son incorrectos', parent=self)

    def register_user(self, username: str, password: str) -> None:

        res = self.auth.register_user(username, password)

        if res:
            messagebox.showinfo('Usuario registrado', 'El usuario ha sido registrado', parent=self)
            self.show_frame('LoginScreen')
        else:
            messagebox.showerror('Error', 'Ocurrió un error al registrar el usuario', parent=self)
