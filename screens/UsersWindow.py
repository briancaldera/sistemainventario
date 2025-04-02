import tkinter as tk

from model.user import User
from screens.UsersScreen import UsersScreen

from services.UserService import UserService


class UsersWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('Panel de usuarios')
        self.resizable(False, False)
        self.geometry("1100x700+120+20")
        self._user_service = UserService()

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in tuple([UsersScreen]):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky='nsew')

            self.show_frame('UsersScreen')  # Mostrar LoginScreen al inicio

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def load_users(self) -> list[User]:
        return self._user_service.get_users()

    def update_role(self, username: str, new_role: str) -> bool:

        try:
            self._user_service.update_role(username, new_role)
        except Exception as e:
            print(f'Error al actualizar el rol del usuario {username}')
            print(e)
            return False

        return True