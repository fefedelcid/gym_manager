from tkinter.ttk import Treeview
from tkinter import StringVar
from customtkinter import CTkFrame, CTkEntry
from src.database import Database
from src.utils import parse_date, get_tag
from datetime import datetime

class ClientsTable(CTkFrame):
    def __init__(self, master, callback=None, mode="clients", *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(corner_radius=0, fg_color="transparent")
        self.mode = mode

        if self.mode == "clients":
            self.config_mode = {
                "columns": ('createdAt', 'fullName', 'document'),
                "configure": self.clients_mode
                }
        elif self.mode == "payments":
            self.config_mode = {
                "columns":('lastPayment', 'fullName', 'phone', 'document'),
                "configure": self.payments_mode
                }
        else:
            raise ValueError("Modo inválido.")

        self.callback = callback

        # Cuadro de búsqueda
        self.search_text = StringVar(self, "")
        self.entry = CTkEntry(self, width=650, height=40, corner_radius=5, placeholder_text="Buscar por DNI, Nombre o Email")
        self.entry.pack(side='top', pady=10)
        self.entry.bind("<KeyRelease>", self.on_search_change)

        # Tabla
        self.table = Treeview(self)
        self.table.pack(anchor="center", fill="both", expand=True)
        self.table.bind("<<TreeviewSelect>>", self.item_selected)

        # Columnas
        self.table["columns"] = self.config_mode["columns"]
        self.table.column('#0', width=0, stretch=False) # Indice oculto
        self.config_mode["configure"]() # Configurar según el modo

        # Configurar estilo para filas por vencer
        self.table.tag_configure('to_expire', background='#FFC300', foreground='#000000')
        # Configurar estilo para filas vencidas
        self.table.tag_configure('expired', background='#ff3333', foreground='#ffffff')
        # Configurar estilo para nuevos alumnos
        self.table.tag_configure('need_check', background='#bb23e6', foreground='#ffffff')

        self.update_table()

    def clients_mode(self):
        self.table.column('createdAt', anchor='center', width=100)
        self.table.column('fullName', anchor='w', width=200)
        self.table.column('document', anchor='center', width=100)

        # Encabezados
        self.table.heading('#0', text="")
        self.table.heading('createdAt', text="Fecha de Registro", anchor='center', command=lambda: self.sort_column('createdAt', True))
        self.table.heading('fullName', text="Nombre y Apellido", anchor='center', command=lambda: self.sort_column('fullName', True))
        self.table.heading('document', text="Documento", anchor='center')


    def payments_mode(self):
        self.table.column('lastPayment', anchor='center', width=100)
        self.table.column('fullName', anchor='w', width=200)
        self.table.column('phone', anchor='center', width=100)
        self.table.column('document', anchor='center', width=100)

        # Encabezados
        self.table.heading('#0', text="")
        self.table.heading('lastPayment', text="Último Pago", anchor='center', command=lambda: self.sort_column('lastPayment', True))
        self.table.heading('fullName', text="Nombre y Apellido", anchor='center', command=lambda: self.sort_column('fullName', True))
        self.table.heading('phone', text="Teléfono", anchor='center')
        self.table.heading('document', text="Documento", anchor='center')

    def on_search_change(self, event):
        """Actualizar la tabla según el término de búsqueda."""
        search_term = self.entry.get()
        self.update_table(search_term)

    def update_table(self, search_term:str=""):
        """Carga los datos de la base de datos y los muestra en la tabla."""
        try:
            self.table.delete(*self.table.get_children()) # Limpiar la tabla
            db = Database()

            if self.mode == "clients":
                if not search_term:
                    clients = db.get_all_clients()
                else:
                    clients = db.search_client(search_term)
                for client in clients:
                    values = (client.createdAt.strftime("%d/%m/%Y"), client.fullName, client.document)
                    tags = get_tag(client)
                    self.table.insert("", "end", values=values, tags=tags)

            elif self.mode == "payments":
                payments = db.get_all_payments()
                for payment in payments:
                    client = db.get_client_by_id(payment.clientId)
                    values = (payment.createdAt.strftime("%d/%m/%Y"), client.fullName, client.phone, client.document)
                    tags = get_tag(client)
                    self.table.insert("", "end", values=values, tags=tags)
        except Exception as e:
            print(f'[Exception] on: update_table, {e}')
    

    def sort_column(self, col, reverse):
        """Ordena la tabla por la columna seleccionada."""
        try:            
            # Obtener los datos y convertir la columna si es fecha
            if col in ['lastPayment', 'createdAt']:
                data = [(parse_date(self.table.set(child, col)), child) for child in self.table.get_children()]
            else:
                data = [(self.table.set(child, col), child) for child in self.table.get_children()]
            data.sort(reverse=reverse, key=lambda x: x[0] if isinstance(x[0], (str, datetime)) else "")
            
            # Reordenar los elementos en la tabla
            for index, (val, kid) in enumerate(data):
                self.table.move(kid, "", index)

            # Cambiar el evento de ordenación
            self.table.heading(col, command=lambda: self.sort_column(col, not reverse))
        except Exception as e:
            print(f"[Exception] on: sort_column, {e}")


    def item_selected(self, event=None):
        """Ejecuta una acción al seleccionar un elemento."""
        try:
            selected_item = self.table.focus()
            if not selected_item:
                return
            values = self.table.item(selected_item, "values")
            document = values[-1] # Último valor es el documento
            if self.callback:
                self.callback(data=document)
        except Exception as e:
            print(f'[Exception] on: item_selected, {e}')
