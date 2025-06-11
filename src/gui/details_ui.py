from customtkinter import CTkFrame, CTkLabel
from src.gui.widgets import MainFrame, StatefulBtn, ClienteForm, PagosForm, FichaForm, DangerBtn
from src.database import Database, Cliente
from datetime import datetime
from src.utils import print_log, parse_date

class DetailsFrame(CTkFrame):
    def __init__(self, master, name, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.name = name
        self.clientId = None
        self.update_callback = None
        self.fields = {}
        self.modo_creacion = False  # Nuevo estado
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
        DangerBtn(self.extra_btns_frame, text="Eliminar alumno", command=self.eliminar_alumno).pack(pady=10)

        self.selected_form("ClientForm")

    def esta_editando(self) -> bool:
        '''Retorna True si el modo edicion se encuentra activo'''
        return (
            getattr(self.client_form, "enabled", False) or
            getattr(self.ficha_form, "enabled", False)
        )

    def selected_form(self, form_name):
        self.controller.show_frame(form_name)
        self.btn_client.state = form_name == "ClientForm"
        self.btn_ficha.state = form_name == "FichaForm"
        self.btn_pagos.state = form_name == "PagosForm"
        self.btn_client.update_color()
        self.btn_ficha.update_color()
        self.btn_pagos.update_color()

    def nuevo_cliente(self):
        self.clientId = None
        self.modo_creacion = True
        self.title.configure(text="Nuevo Cliente")
        self.client_form.generate_form(Cliente())
        if self.client_form.enabled:
            self.client_form.edit_mode()
        self.ficha_form.generate_form(None)
        if self.ficha_form.enabled:
            self.ficha_form.edit_mode()
        self.pagos_form.update_table([])
        self.selected_form("ClientForm")

    def populate(self, document):
        db = Database()
        client = db.get_client(document)
        self.clientId = client.id
        ficha = db.get_ficha(client.id)
        pagos = db.get_payments(client.id)

        self.title.configure(text=client.fullName)
        self.client_form.generate_form(client)
        self.ficha_form.generate_form(ficha)
        self.pagos_form.update_table(pagos)
        self.modo_creacion = False
        self.selected_form("ClientForm")

    def eliminar_alumno(self):
        db = Database()
        db.delete_client(self.clientId)
        self.master.show_frame("StudentsFrame")
        if self.update_callback:
            self.update_callback()

    def registrar_pago(self, amount: float, createdAt: datetime = None):
        db = Database()
        db.add_payment(clientId=self.clientId, amount=amount, date=createdAt)
        pagos = db.get_payments(self.clientId)
        self.pagos_form.update_table(pagos)
        if self.update_callback:
            self.update_callback()

    def guardar_ficha(self, **ficha):
        db = Database()
        print_log(f"[DEBUG] Datos recibidos para guardar_ficha: {ficha}")
        db.update_ficha(self.clientId, **ficha)
        if self.update_callback:
            self.update_callback()

    def guardar_datos(self, **data):
        db = Database()
        print_log(f"[DEBUG] Datos recibidos para guardar_datos: {data}")
        try:
            for field in ["createdAt", "birthDate", "lastPayment"]:
                if field in data:
                    data[field] = parse_date(data[field]) if data[field] else None  # 👈 esto es clave
            if field == "lastPayment":
                data["lastPayment"] = data["lastPayment"] or datetime.now()
                print_log(f"[DEBUG] lastPayment ajustado a: {data['lastPayment']}")
                
            if self.clientId is None:
                cliente = Cliente(**data)
                cliente = db.add_client(cliente)
                if cliente:
                    self.clientId = cliente.id
                    self.title.configure(text=cliente.fullName)
                    self.modo_creacion = False
            else:
                db.update_client(self.clientId, **data)
            if self.update_callback:
                self.update_callback()
        except Exception as e:
            print_log(f"[Exception] {e.args}")