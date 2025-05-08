import tkinter as tk
from db.database import Database
from tkinter import messagebox


class ConfigScreen(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Configuración")
        self.geometry("400x300")
        self.resizable(False, False)

        # Aquí puedes agregar los widgets de configuración
        label = tk.Label(self, text="Configuración", bg="#6CD9E3", font=("Arial", 16))
        label.pack(pady=20)

        # Botón para cerrar la ventana de configuración
        close_button = tk.Button(self, text="Cerrar", command=self.destroy)
        close_button.pack(pady=10)

        backup_label = tk.Label(self, text="Realizar copia de seguridad", bg="#6CD9E3", font=("Arial", 12))
        backup_label.pack(pady=10)
        backup_button = tk.Button(self, text="Hacer Backup", command=self.backup_database)
        backup_button.pack(pady=10)

    def backup_database(self):
        res = Database.backup()
        if res:
            tk.messagebox.showinfo("Backup", "Copia de seguridad realizada con éxito.", parent=self)
        else:
            tk.messagebox.showerror("Backup", "Error al realizar la copia de seguridad.", parent=self)