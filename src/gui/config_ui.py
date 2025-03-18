from customtkinter import CTkFrame, CTkLabel


class ConfigFrame(CTkFrame):
    def __init__(self, master, name, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(corner_radius=0)
        self.name = name
        CTkLabel(self, font=("Roboto", 32), text=self.name).pack(side="top")