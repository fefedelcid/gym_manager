from customtkinter import CTkFrame, CTkLabel
from src.gui.widgets import ClientsTable

class ClientsFrame(CTkFrame):
    def __init__(self, master, name, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(corner_radius=0)
        self.name = name

        self.title = CTkLabel(self, text="Listado de Alumnos", font=('', 36))
        self.title.pack(side="top", pady=10)

        self.table = ClientsTable(self, self.callback)
        self.table.pack(fill='both', expand=True)

    def callback(self, event=None, data:str=None):
        """Este método se ejecuta al seleccionar un registro en
        ClientsTable.item_selected.
        :data: Mismo que Cliente.document"""
        print(f"ClientsFrame.callback, data:{data}")
        self.master.show_frame("DetailsFrame", data)