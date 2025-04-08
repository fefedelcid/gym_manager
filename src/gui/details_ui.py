from customtkinter import CTkFrame, CTkLabel
from src.gui.widgets import MainFrame, StatefulBtn, ClienteForm, PagosForm, FichaForm, DangerBtn
from src.database import Database
from datetime import datetime

class DetailsFrame(CTkFrame):
    def __init__(self, master, name, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.name = name
        self.clientId = None
        self.update_callback = None
        self.fields = {}

        self.title = CTkLabel(self, text="Seleccionar cliente", font=("", 32))
        self.title.pack(pady=10)

        # Formulario izquierdo
        self.controller = MainFrame(self)
        self.controller.pack(side="left", fill="both", expand=True)

        self.client_form = self.controller.add_frame("ClientForm", ClienteForm)
        self.client_form.callback = self.guardar_datos
        
        self.ficha_form = self.controller.add_frame("FichaForm", FichaForm)
        self.ficha_form.callback = self.guardar_ficha
        
        self.pagos_form = self.controller.add_frame("PagosForm", PagosForm)
        self.pagos_form.callback = self.registrar_pago
        
        self.controller.show_frame("ClientForm")

        # Botonera derecha
        self.right_frame = CTkFrame(self, fg_color="transparent", width=450)
        self.right_frame.pack(side="right", fill="y", padx=50)

        self.form_btns_frame = CTkFrame(self.right_frame, fg_color="transparent")
        self.form_btns_frame.pack(side="top", pady=20)

        self.extra_btns_frame = CTkFrame(self.right_frame, fg_color="transparent")
        self.extra_btns_frame.pack(side="bottom", pady=20)

        # Cambio de formularios
        self.btn_client = StatefulBtn(self.form_btns_frame, text="Datos Personales", command=lambda: self.selected_form("ClientForm"))
        self.btn_client.pack(pady=10)
        
        self.btn_ficha = StatefulBtn(self.form_btns_frame, text="Ficha Médica", command=lambda: self.selected_form("FichaForm"))
        self.btn_ficha.pack(pady=10)
        
        self.btn_pagos = StatefulBtn(self.form_btns_frame, text="Historial de Pagos", command=lambda: self.selected_form("PagosForm"))
        self.btn_pagos.pack(pady=10)

        # Acciones sobre los datos
        # --- Eliminar alumno ---
        DangerBtn(self.extra_btns_frame, text="Eliminar alumno", command=self.eliminar_alumno).pack(pady=10)

        # --- Limpiar cambios ---
        self.selected_form("ClientForm")
        
    def selected_form(self, form_name):
        self.controller.show_frame(form_name)
        if form_name=="ClientForm":
            self.btn_client.state=True
            self.btn_client.update_color()
            self.btn_ficha.state=False
            self.btn_ficha.update_color()
            self.btn_pagos.state=False
            self.btn_pagos.update_color()
        elif form_name=="FichaForm":
            self.btn_client.state=False
            self.btn_client.update_color()
            self.btn_ficha.state=True
            self.btn_ficha.update_color()
            self.btn_pagos.state=False
            self.btn_pagos.update_color()
        elif form_name=="PagosForm":
            self.btn_client.state=False
            self.btn_client.update_color()
            self.btn_ficha.state=False
            self.btn_ficha.update_color()
            self.btn_pagos.state=True
            self.btn_pagos.update_color()

    def populate(self, document=None):
        """Este método completa los 3 formularios según el cliente seleccionado."""
        if document:
            db = Database()
            client = db.get_client(document)
            self.clientId = client.id
            ficha = db.get_ficha(client.id)
            pagos = db.get_payments(client.id)

            self.title.configure(text=client.fullName)
        else:
            self.title.configure(text="Agregar Cliente")

        self.client_form.generate_form(None if document is None else client)
        self.ficha_form.generate_form(None if document is None else ficha)
        self.pagos_form.update_table([] if document is None else pagos)
        
        self.selected_form("ClientForm")

    def eliminar_alumno(self):
        db = Database()
        db.delete_client(self.clientId)
        self.master.show_frame("StudentsFrame")
        if self.update_callback:
            self.update_callback()
    
    def registrar_pago(self, amount:float, createdAt:datetime=None):
        db = Database()
        db.add_payment(clientId=self.clientId, amount=amount, date=createdAt)
        pagos = db.get_payments(self.clientId)
        self.pagos_form.update_table(pagos)
        if self.update_callback:
            self.update_callback()

    def guardar_ficha(self, **ficha):
        db = Database()
        db.update_ficha(self.clientId, **ficha)
        if self.update_callback:
            self.update_callback()

    def guardar_datos(self, **data):
        db = Database()
        db.update_client(self.clientId, **data)
        if self.update_callback:
            self.update_callback()