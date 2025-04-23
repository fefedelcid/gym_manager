from customtkinter import CTkFrame
from tkinter import messagebox
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
        # ⚠️ Si hay un DetailsFrame en edición, no permitir cambiar
        new_student, details = None, None
        if "DetailsFrame" in self.frames.keys():
            details = self.frames["DetailsFrame"]
        if "NewStudentFrame" in self.frames.keys():
            new_student = self.frames["NewStudentFrame"]

        if hasattr(new_student, "esta_editando") and hasattr(details, "esta_editando"):
            print_log(f"[DEBUG] flag:{details.esta_editando() and new_student.esta_editando()}")
            if details.esta_editando() or new_student.esta_editando():
                messagebox.showwarning(
                    "Edición activa",
                    "Debes guardar o cancelar los cambios antes de continuar."
                )
                return  # ⛔ No cambiamos el frame

        for frame in self.frames.values():
            frame.pack_forget()
        try:
            print_log(f"frame:{name}, data:{data}")
            if name=="DetailsFrame" and data:
                self.frames[name].populate(data)
            elif name=="NewStudentFrame":
                self.frames[name].nuevo_cliente()

            self.frames[name].pack(fill="both", expand=True)
        except KeyError:
            print_log("[WARNING] Pestaña no encontrada.")
        except Exception as e:
            print_log(f"[Exception] {e.args}")