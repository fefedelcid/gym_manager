from customtkinter import CTkFrame
from src.utils import print_log

class MainFrame(CTkFrame):
    """Esta clase ayuda a manejar múltiples vistas de forma sencilla."""

    def __init__(self, master, *args, **kwargs):
        super().__init__(master,*args, **kwargs)
        self.configure(corner_radius=0)
        self.frames = {}
    
    def add_frame(self, name, frame_class):
        """Agrega un frame al contenedor"""
        frame = frame_class(self, name)

        self.frames[name] = frame
        frame.pack(fill="both", expand=True)
        frame.pack_forget() # Ocultar inicialmente
        return frame

    def show_frame(self, name, data=None):
        """Muestra solo el frame seleccionado"""
        for frame in self.frames.values():
            frame.pack_forget()
        try:
            print_log(f"frame:{name}, data:{data}")
            if name=="DetailsFrame" and data:
                self.frames[name].populate(data)
            self.frames[name].pack(fill="both", expand=True)
        except KeyError:
            print_log("Pestaña no encontrada.")