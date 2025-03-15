import tkinter as tk
from typing import override

from auth.AuthManager import AuthManager
from event.EventQueue import EventQueue
from event.EventSubscriber import EventSubscriber
from screens.LoginScreen import LoginScreen
from screens.RegisterScreen import RegisterScreen


class HomeWindow(tk.Tk, EventSubscriber):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('Sistema de inventario')
        self.resizable(False, False)
        self.geometry("400x400+120+20")

        self.auth = AuthManager.get_instance()
        event_queue = EventQueue.get_instance()

        event_queue.subscribe(self, 'user-logout')

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # self.routes = {
        #     'login': LoginScreen,
        #     'register': RegisterScreen
        # }

        self.frames = {}
        for F in (LoginScreen, RegisterScreen):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky='nsew')
        # self.to_route('login')

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def login_user(self, username: str, password: str) -> bool:
        return self.auth.login(username, password)

    def register_user(self, username: str, password: str) -> bool:
        return self.auth.register_user(username, password)

    @override
    def receive(self, message: str):
        if message == 'user-logout':
            self.destroy()


def main():
    app = HomeWindow()
    app.mainloop()

if __name__ == "__main__":
    main()
