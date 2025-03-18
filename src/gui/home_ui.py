from customtkinter import CTkFrame, CTkLabel


class HomeFrame(CTkFrame):
    def __init__(self, master, name, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(corner_radius=0)
        self.name = name

        self.title = CTkLabel(self, font=('Roboto', 56), text="OXYS GYM")
        self.title.pack(pady=50, anchor="center")

        self.subtitle = CTkLabel(self, font=('Roboto', 16), text="Sistema Administrativo")
        self.subtitle.pack()