from customtkinter import CTkScrollableFrame, CTkFrame, CTkEntry, CTkLabel, CTkButton
from src.database import Cliente, Ficha, Movimiento
from src.gui.widgets import EntryDate, MoneyEntry, StatefulBtn
from tkinter.ttk import Treeview
from src.utils import parse_date, print_log
from datetime import datetime

class BaseForm:
    def __init__(self, master, name, callback=None, *args, **kwargs):
        self.master = master
        self.callback = callback
        self.configure(corner_radius=0, fg_color="transparent")
        self.name = name
        self.fields:dict[str,CTkEntry] = {}
        self.enabled = False
        self.btn:StatefulBtn = None

    def add_switch(self, cb=None):
        frame = CTkFrame(self, fg_color="transparent")
        frame.pack(fill="x", pady=5)
        self.btn = StatefulBtn(frame, False, command=lambda: self.edit_mode(cb), text="Editar")
        self.btn.pack()

    def add_field(self, label, value=""):
        frame = CTkFrame(self, fg_color="transparent")
        frame.pack(fill="x", padx=10, pady=5)

        lbl = CTkLabel(frame, text=label+":", font=("", 16))
        lbl.pack(side="top", pady=5, anchor="w")

        entry = CTkEntry(frame, font=("", 14))
        entry.insert(0, str(value) if value is not None else "")
        entry.configure(state="disabled")
        entry.pack(side="top", fill="x", expand=True)
        
        self.fields[label] = entry

    def edit_mode(self, cb=None):
        self.enabled = not self.enabled
        print_log(f"[DEBUG] enabled:{self.enabled}")

        state = "normal" if self.enabled else "disabled"
        if self.btn:
            self.btn.configure(text="Editar" if state=="disabled" else "Guardar")
            self.btn.state = self.enabled
            if not self.enabled and cb: cb()
        for key, entry in self.fields.items():
            if key in ["Último pago", "Inscripto desde", "Email"]: continue
            entry.configure(state=state, border_color='#ff3636' if state=="normal" else '#565B5E')

    def refresh(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.fields.clear()


class ClienteForm(CTkScrollableFrame, BaseForm):
    def __init__(self, master, name, *args, **kwargs):
        CTkScrollableFrame.__init__(self, master, *args, **kwargs)
        BaseForm.__init__(self, master, name, *args, **kwargs)

    def generate_form(self, client:Cliente):
        self.refresh()
        self.add_switch(self.guardar_cambios)
        self.add_field("Inscripto desde", client.createdAt)
        self.add_field("Nombre Completo", client.fullName)
        self.add_field("Fecha de Nacimiento", client.birthDate)
        self.add_field("Documento", client.document)
        self.add_field("Género", client.gender)
        self.add_field("Email", client.email)
        self.add_field("Teléfono", client.phone)
        self.add_field("Dirección", client.address)
        self.add_field("Último pago", client.lastPayment)
        self.add_field("Objetivo", client.goal)

    def guardar_cambios(self):
        try:
            datos = {
                "createdAt":parse_date(self.fields["Inscripto desde"].get()),
                "fullName":self.fields["Nombre Completo"].get(),
                "birthDate":parse_date(self.fields["Fecha de Nacimiento"].get()),
                "document":self.fields["Documento"].get(),
                "gender":self.fields["Género"].get(),
                "email":self.fields["Email"].get(),
                "phone":self.fields["Teléfono"].get(),
                "address":self.fields["Dirección"].get(),
                "lastPayment":self.fields["Último pago"].get(),
                "goal":self.fields["Objetivo"].get()
            }
            self.callback(**datos)
        except Exception as e:
            print_log(f"[Exception] {e.args}")
            if self.enabled:
                self.edit_mode()


class FichaForm(CTkScrollableFrame, BaseForm):
    def __init__(self, master, name, *args, **kwargs):
        CTkScrollableFrame.__init__(self, master, *args, **kwargs)
        BaseForm.__init__(self, master, name, *args, **kwargs)

    def generate_form(self, ficha:Ficha|None):
        self.refresh()
        self.add_switch(self.guardar_cambios)
        self.add_field("Historial Médico", ficha.medicalHistory if ficha else "")
        self.add_field("Medicación", ficha.medication if ficha else "")
        self.add_field("Lesión Reciente", ficha.recentInjury if ficha else "")
        self.add_field("Contacto de Emergencia", ficha.emergencyContact if ficha else "")
        self.add_field("Certificado Médico", ficha.medicalCertificate if ficha else "")

    def guardar_cambios(self):
        try:
            ficha = {
                "medicalHistory": self.fields["Historial Médico"].get(),
                "medication": self.fields["Medicación"].get(),
                "recentInjury": self.fields["Lesión Reciente"].get(),
                "emergencyContact": self.fields["Contacto de Emergencia"].get(),
                "medicalCertificate": self.fields["Certificado Médico"].get()
            }
            self.callback(**ficha)
        except Exception as e:
            print_log(f"[Exception] {e.args}")
            if self.enabled:
                self.edit_mode()



class PagosForm(CTkFrame, BaseForm):
    def __init__(self, master, name, *args, **kwargs):
        CTkFrame.__init__(self, master, *args, **kwargs)
        BaseForm.__init__(self, master, name, *args, **kwargs)

        # Registrar pago nuevo
        payment_frame = CTkFrame(self, fg_color="transparent", corner_radius=0)
        payment_frame.pack(side="top", pady=20)

        CTkLabel(payment_frame, text="Monto:").grid(column=0, row=0, padx=50, pady=5)
        self.amount = MoneyEntry(payment_frame)
        self.amount.grid(column=0, row=1)
        
        CTkLabel(payment_frame, text="Fecha de pago:").grid(column=1, row=0, padx=50, pady=5)
        self.createdAt = EntryDate(payment_frame)
        self.createdAt.grid(column=1, row=1)

        self.alert = CTkLabel(payment_frame, text="", text_color="red")
        self.alert.grid(column=3, row=0, columnspan=2)
        CTkButton(payment_frame, text="Registrar Pago", command=self.register_payment).grid(column=3, row=1, pady=5, padx=25)


        # Configuración de la tabla
        self.table = Treeview(self)
        self.table.pack(fill="both", expand=True)
        self.table.bind("<<TreeviewSelect>>", self.item_selected)

        # Columnas
        self.table["columns"] = ("createdAt", "amount")
        self.table.column("#0", width=0, stretch=False) # Indice oculto
        self.table.column("createdAt", anchor="center")
        self.table.column("amount", anchor="center")

        # Encabezados
        self.table.heading("#0", text="")
        self.table.heading("createdAt", text="Fecha del Pago", anchor="center",\
                            command=lambda: self.sort_column("createdAt", True))
        self.table.heading("amount", text="Cantidad Abonada", anchor="center")

    def register_payment(self):
        try:
            createdAt, amount = self.createdAt.get(), self.amount.get()
            if createdAt and amount:
                self.callback(createdAt=createdAt, amount=amount)
                self.alert.configure(text="")
                self.amount.clear()
            elif not createdAt:
                self.alert.configure(text="La fecha ingresada es incorrecta.")
            elif not amount:
                self.alert.configure(text="El monto ingresado es inválido.")
        except Exception as e:
            print_log(f"[Exception] {e.args}")

    def sort_column(self, col, reverse):
        try:
            if col=='createdAt':
                data = [(parse_date(self.table.set(child, col)), child) for child in self.table.get_children()]
            else:
                data = [(self.table.set(child, col), child) for child in self.table.get_children()]
            data.sort(reverse=reverse, key=lambda x: x[0] if isinstance(x[0], (str, datetime)) else "")
            
            for index, (val, kid) in enumerate(data):
                self.table.move(kid, "", index)
            self.table.heading(col, command=lambda: self.sort_column(col, not reverse))
        except Exception as e:
            print_log(f"[Exception] {e}")

    def item_selected(self, event=None):
        try:
            selected_item = self.table.focus()
            if not selected_item:
                return
            values = self.table.item(selected_item, "values")
            self.createdAt.insert(0, string=values[0])
            self.amount.insert(0, values[1])
        except Exception as e:
            print_log(f"[Exception] {e}")

    def update_table(self, movimientos:list[Movimiento]):
        try:
            self.table.delete(*self.table.get_children()) # Limpiar la tabla
            for pago in movimientos:
                values = (pago.createdAt.strftime("%d/%m/%Y"), pago.amount)
                self.table.insert("", "end", values=values)
        except Exception as e:
            print_log(f"[Exception] {e}")
