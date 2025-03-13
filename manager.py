from tkinter import Tk, Frame
from container import Container
from ttkthemes import ThemedStyle

class Manager(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Sistema de Ventas")
        self.resizable(False, False)
        self.configure(bg="#6CD9E3")  # Los colores en Tkinter deben estar en formato hexadecimal con '#'
        self.geometry("800x400+120+20")

        self.container = Frame(self, bg="#6CD9E3")
        self.container.pack(fill="both", expand=True)

        self.frames = {
            Container: None
        }

        self.load_frames()
        self.show_frame(Container)
        self.set_theme()

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

def main():
    app = Manager()  # Corregido el nombre de la clase
    app.mainloop()

if __name__ == "__main__":
    main()