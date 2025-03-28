from customtkinter import CTkFrame, CTkLabel
from src.gui.widgets import ClientsTable
from src.utils import print_log

class PaymentsFrame(CTkFrame):
    def __init__(self, master, name, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(corner_radius=0)
        self.name = name

        self.title = CTkLabel(self, text="Historial de Pagos", font=('', 36))
        self.title.pack(side="top", pady=10)

        self.table = ClientsTable(self, self.callback, mode="payments")
        self.table.pack(fill='both', expand=True)

    def callback(self, event=None, data=None):
        self.client_dni = data
        print_log(data)