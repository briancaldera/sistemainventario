import tkinter as tk
from tkinter import Toplevel

from auth.AuthManager import AuthManager
from container import Container
from screens.RegisterScreen import RegisterScreen


class LoginScreen(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent, background='#6CD9E3')
        self.controller = controller

        self.pack()


        self._widgets()



    def _widgets(self):
        self.title_label = tk.Label(self, text='Iniciar sesión')
        self.title_label.pack()
        self.username_label = tk.Label(self, text='Usuario:')
        self.username_label.pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        self.password_label = tk.Label(self, text='Contraseña:')
        self.password_label.pack()
        self.password_entry = tk.Entry(self)
        self.password_entry.pack()

        self.login_button = tk.Button(self, text='Iniciar sesión', command=self.login_user)
        self.login_button.pack()

        self.register_button = tk.Button(self, text='Registrar', command=lambda: self.controller.show_frame('RegisterScreen'))
        self.register_button.pack()

    def login_user(self):
        res = self.controller.login_user(self.username_entry.get(), self.password_entry.get())

def main():
    app = tk.Tk()
    app.title('Iniciar sesión')
    app.resizable(False, False)
    app.configure(bg="#6CD9E3")
    app.geometry("400x400+120+20")
    frame = LoginScreen(app)
    frame.tkraise()
    app.mainloop()

if __name__ == "__main__":
    main()