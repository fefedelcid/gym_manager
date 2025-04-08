from customtkinter import CTkFrame, CTkLabel, CTkButton
from src.core import sync_google_sheets
from src.utils.logs_tracker import send_today_log


class HomeFrame(CTkFrame):
    def __init__(self, master, name, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(corner_radius=0)
        self.name = name

        self.title = CTkLabel(self, font=('Roboto', 56), text="OXYS GYM")
        self.title.pack(pady=50, anchor="center")

        self.subtitle = CTkLabel(self, font=('Roboto', 16), text="Sistema Administrativo")
        self.subtitle.pack()

        self.frame = CTkFrame(self, fg_color="transparent")
        self.frame.pack(side="bottom", pady=100)

        self.sync_btn = CTkButton(self.frame, height=50, font=('Roboto', 16), text="Sincronizar\nFichas", command=sync_google_sheets)
        self.sync_btn.grid(column=0, row=0, sticky="e", ipadx=15, padx=50)

        self.send_btn = CTkButton(self.frame, height=50, font=('Roboto', 16), text="Enviar Logs", command=send_today_log)
        self.send_btn.grid(column=1, row=0, sticky="w", ipadx=15, padx=50)