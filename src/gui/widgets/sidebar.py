from customtkinter import CTkFrame
from src.gui.widgets import IconButton

class SideBar(CTkFrame):
    def __init__(self, master, controller, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(fg_color='#4F7399', corner_radius=0)
        self.controller = controller
        
        size=48

        self.icons = [
            IconButton(self, f'assets/icons/icons8-casa-{size}.png', 'HomeFrame', self.controller), # Inicio
            IconButton(self, f'assets/icons/icons8-contactos-{size}.png', 'StudentsFrame', self.controller), # Alumnos
            IconButton(self, f'assets/icons/icons8-info-{size}.png', 'DetailsFrame', self.controller), # Detalles
            IconButton(self, f'assets/icons/icons8-currency-{size}.png', 'PaymentsFrame', self.controller), # Caja
            IconButton(self, f'assets/icons/icons8-whatsapp-{size}.png', 'whatsapp', self.controller), # Whatsapp
            IconButton(self, f'assets/icons/icons8-ajustes-{size}.png', 'ConfigFrame', self.controller), # Configuración
            IconButton(self, f'assets/icons/icons8-exit-{size}.png', 'salir', callback=self.master.quit) # Salir
        ]

        self.icons[0].pack(side="top", padx=1, pady=16) # Inicio
        self.icons[1].pack(side="top", padx=1, pady=16) # Alumnos
        self.icons[3].pack(side="top", padx=1, pady=16) # Caja
        self.icons[2].pack(side="top", padx=1, pady=16) # Detalles
        # self.icons[4].pack(side="top", padx=1, pady=16) # Whatsapp
        self.icons[6].pack(side="bottom", padx=1, pady=16) # Salir
        # self.icons[5].pack(side="bottom", padx=1, pady=16) # Configuración


