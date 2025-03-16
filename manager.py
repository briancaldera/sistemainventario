from tkinter import Tk, Frame
from typing import override

from auth.AuthManager import AuthManager
from container import Container
from ttkthemes import ThemedStyle

from event.EventQueue import EventQueue
from event.EventSubscriber import EventSubscriber
from tkinter import messagebox


class Manager(Tk, EventSubscriber):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Sistema de Ventas")
        self.resizable(False, False)
        self.configure(bg="#6CD9E3")  # Los colores en Tkinter deben estar en formato hexadecimal con '#'
        self.geometry("800x400+120+20")

        self.container = Frame(self, bg="#6CD9E3")
        self.container.pack(fill="both", expand=True)

        self.auth = AuthManager.get_instance()

        event_queue = EventQueue.get_instance()
        event_queue.subscribe(self, 'user')

        self.frames = {
            Container: None
        }

        self.load_frames()
        self.show_frame(Container)
        self.set_theme()

    def logout(self):
        self.auth.logout()

    def load_frames(self):
        for frame_class in self.frames.keys():  # Corregido el nombre de la variable
            frame = frame_class(self.container, self)
            self.frames[frame_class] = frame
            

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()

    def set_theme(self):
        style = ThemedStyle(self)   
        style.set_theme("breeze")

    @override
    def receive(self, message: str):
        if message == 'user-logout':
            messagebox.showinfo('Cerrando sesión', 'Sesión cerrada')
            self.destroy()

def main():
    app = Manager()  # Corregido el nombre de la clase
    app.mainloop()

if __name__ == "__main__":
    main()