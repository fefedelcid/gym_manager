from src.config.settings import WIDTH, HEIGHT, APPEARANCE_MODE, COLOR_THEME, TITLE
from customtkinter import CTk, set_appearance_mode, set_default_color_theme
from src.gui import HomeFrame, ClientsFrame, PaymentsFrame, ConfigFrame, DetailsFrame
from src.gui.widgets import MainFrame, SideBar
from src.utils import get_center, print_log

set_appearance_mode(APPEARANCE_MODE)
set_default_color_theme(COLOR_THEME)

class MainWindow(CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Dimensiones y posición
        self.geometry(get_center(self, width=WIDTH, height=HEIGHT))

        # Configuraciones adicionales
        self.title(TITLE)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.resizable(False, False)

        # Vistas
        self.mainframe = MainFrame(self)
        self.mainframe.grid(row=0, column=1, sticky="nsew")

        # Página de inicio
        self.mainframe.add_frame("HomeFrame", HomeFrame)
        # Página de estudiantes
        self.clients_frame = self.mainframe.add_frame("StudentsFrame", ClientsFrame)
        details = self.mainframe.add_frame("DetailsFrame", DetailsFrame)
        details.update_callback = self.update_tables
        # Página de pagos
        self.payments_frame = self.mainframe.add_frame("PaymentsFrame", PaymentsFrame)
        # Página de configuración
        # self.mainframe.add_frame("ConfigFrame", ConfigFrame)
        
        self.mainframe.show_frame("HomeFrame")

        # Menú lateral
        self.sidebar = SideBar(self, self.mainframe)
        self.sidebar.grid(row=0, column=0, sticky="ns")

    def update_tables(self):
        self.clients_frame.table.update_table()
        self.payments_frame.table.update_table()

    def destroy(self):
        print_log("[INFO] Cerrando aplicación.")
        super().destroy()