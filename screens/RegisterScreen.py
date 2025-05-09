import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showerror, showinfo

from auth.AuthManager import AuthManager


class RegisterScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.widgets()
        self.auth = AuthManager.get_instance()
        self.title('Registrar usuario')
        self.resizable(False, False)
        self.geometry('400x300+500+200')

    def widgets(self):
        # Frame para el título (frame2)
        frame2 = tk.Frame(self, bg="#C6D9E3", highlightbackground="gray", highlightthickness=1)
        frame2.place(x=0, y=0, relwidth=1, height=90)

        self.title_label = ttk.Label(frame2, text='Registrar usuario', font=('Arial', 16, 'bold'))
        self.title_label.place(relx=0.5, rely=0.5, anchor='center')

        # Frame para el resto de los widgets (frame1)
        frame1 = tk.Frame(self, bg='#E0F2F7')
        frame1.place(x=0, y=90, relwidth=1, relheight=1)

        self.username_label = ttk.Label(frame1, text='Usuario:')
        self.username_label.place(x=50, y=10)
        self.username_entry = ttk.Entry(frame1)
        self.username_entry.place(x=150, y=10)

        self.password_label = ttk.Label(frame1, text='Contraseña:')
        self.password_label.place(x=50, y=60)
        self.password_entry = ttk.Entry(frame1, show='*')
        self.password_entry.place(x=150, y=60)

        self.register_button = ttk.Button(frame1, text='Registrar', command=self.register_user)
        self.register_button.place(relx=0.5, y=110, anchor='center')


    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            self.auth.register_user(username, password)
            showinfo('Usuario registrado', 'Usuario registrado exitosamente')
        except Exception as e:
            print(e)
            showerror('Error', 'Ocurrió un error al intentar registrar al usuario')
