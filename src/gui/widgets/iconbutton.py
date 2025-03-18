from PIL import Image
from customtkinter import CTkButton, CTkImage

class IconButton(CTkButton):
    def __init__(self, master, img_path, name, controller=None, size=(48, 48), callback=None, *args, **kwargs):
        img = Image.open(img_path)

        self.icon = CTkImage(
            light_image=img,
            dark_image=img,
            size=size
        )
        self.user_callback = callback
        self.name = name
        self.controller = controller
        
        super().__init__(master, image=self.icon, text="",
                         width=size[0]+15, height=size[1],
                         fg_color="transparent",
                         corner_radius=0, command=self.on_click, *args, **kwargs)
    
    def on_click(self):
        """Método que llama automáticamente a show_frame"""
        if self.controller:
            self.controller.show_frame(self.name)
        elif self.user_callback:
            self.user_callback()