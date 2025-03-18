from customtkinter import CTkButton
from tkinter import messagebox

class StatefulBtn(CTkButton):
    def __init__(self, master, initial_state:bool=True, command=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.state = initial_state
        self.user_command = command
        self.configure(command=self.command_wrapper)
        
    def command_wrapper(self):
        self.change_state()
        if self.user_command:
            self.user_command()

    def change_state(self):
        self.state = not self.state
        self.update_color()

    def update_color(self):
        if self.state:
            self.configure(fg_color=['#D03B3B', '#A51F1F'])
        else:
            self.configure(fg_color=['#3B8ED0', '#1F6AA5'])

class DangerBtn(CTkButton):
    def __init__(self, master, command=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(fg_color=['#D03B3B', '#A51F1F'])
        self.configure(command=self.command_wrapper)
        self.user_command = command
    
    def command_wrapper(self):
        response = messagebox.askokcancel("Confirmación", "¿Estás seguro de que deseas continuar?")
        if response and self.user_command:
            self.user_command()