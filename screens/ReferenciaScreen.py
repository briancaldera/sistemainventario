import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from model.referencia import Referencia
from services.ReferenciaService import ReferenciaService


class ReferenciaScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.referencia_service = ReferenciaService()
        self.referencias: list[Referencia] = []

        self.valor_entry = tk.Entry(self)
        self.valor_entry.pack()

        self.crear_button = tk.Button(self, text='Crear nueva referencia', command=self.on_crear_referencia)
        self.crear_button.pack()

        x_scrollbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        y_scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.referencias_table = ttk.Treeview(self, columns=('Valor', 'Fecha'), show='headings',
                                              xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)
        self.referencias_table.heading('#1', text='Valor')
        self.referencias_table.heading('#2', text='Fecha')

        self.referencias_table.column("#1", anchor="center")
        self.referencias_table.column("#2", anchor="center")

        self.referencias_table.pack(expand=True)

        self.refrescar_lista()

    def on_crear_referencia(self):
        valor = self.valor_entry.get()
        try:
            self.referencia_service.crear_referencia(valor)
            self.refrescar_lista()
            messagebox.showinfo('Referencia creada',
                                'La referencia de cambio ha sido creada y será usada como referencia principal', parent=self)

        except Exception as e:
            print(e)
            messagebox.showerror('Error', 'Ha ocurrido un error al intentar crear la referencia', parent=self)

    def refrescar_lista(self):
        referencias = self.referencia_service.listar()
        self.referencias = referencias

        self.referencias_table.delete(*self.referencias_table.get_children())

        for referencia in referencias:
            self.referencias_table.insert('', 'end', values=(referencia.valor, referencia.created_at))
