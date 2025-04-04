import tkinter as tk
import tkinter.ttk as ttk

class RegisterScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, background='#E0F2F7')
        self.controller = controller
        self.widgets()

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

        self.user_exists_button = ttk.Button(frame1, text='Ya tengo usuario',
                                            command=lambda: self.controller.show_frame('LoginScreen'))
        self.user_exists_button.place(relx=0.5, y=160, anchor='center')

    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.controller.register_user(username, password)
