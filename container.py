from tkinter import *
import tkinter as tk
from ventas import Ventas
from inventario import Inventario
from PIL import Image, ImageTk

class Container(tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        self.pack()
        self.configure(bg="#6CD9E3")  # Los colores en Tkinter deben estar en formato hexadecimal con '#'
        self.place(x=0, y=0, width=800, height=400)
        self.widgets()
        
    def show_frame(self, container):
        Top_level = tk.Toplevel(self)
        frame = container(Top_level)
        frame.config(bg="#6CD9E3")
        frame.pack(fill="both", expand=True)
        Top_level.geometry("1100x650+120+20")
        Top_level.resizable(False, False)

        Top_level.transient(self.master)
        Top_level.grab_set()
        Top_level.focus_set()
        Top_level.lift()

    def ventas(self):
        self.show_frame(Ventas)

    def inventario(self):
        self.show_frame(Inventario)

    def widgets(self):
        frame1 = tk.Frame(self, bg="#C6D9E3")
        frame1.pack()
        frame1.place(x=0, y=0, width=800, height=400)

        btnventas = Button(frame1, bg="#f4b400", fg="white", font="sans 18 bold", text="ir a ventas", command=self.ventas)
        btnventas.place(x=500, y=30, width=240, height=60)

        btninventario = Button(frame1, bg="#c62e26", fg="white", font="sans 18 bold", text="ir a inventario", command=self.inventario)
        btninventario.place(x=500, y=130, width=240, height=60)

        logout_button = Button(frame1, text="Cerrar sesión", command=self.controlador.logout)
        logout_button.place(x=500, y=230, width=240, height=60)

        self.logo_image = Image.open("imagenes/registradora.webp")
        self.logo_image = self.logo_image.resize((280,280))
        self.logo_image = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = Label(frame1, image=self.logo_image, bg="#C6D9E3")
        self.logo_label.place(x=100, y=30, width=280, height=280)

        copyright_label = Label(frame1, text="© 2025 - Todos los derechos reservados", bg="#C6D9E3", fg="gray", font="sans 10")
        copyright_label.place(x=180, y=350)
