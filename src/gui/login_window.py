import tkinter as tk
from tkinter import messagebox
import threading
from src.services import get_google_credentials
from src.services import find_spreadsheet
from src.gui import MainWindow

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login - Gym Manager")
        self.geometry("400x300")
        self.resizable(False, False)
        
        self.label = tk.Label(self, text="Inicia sesión con Google")
        self.label.pack(pady=20)
        
        self.login_button = tk.Button(self, text="Iniciar sesión", command=self.authenticate)
        self.login_button.pack(pady=10)
    
    def authenticate(self):
        threading.Thread(target=self.auth_process, daemon=True).start()
    
    def auth_process(self):
        creds = get_google_credentials()
        if creds:
            self.destroy()
            MainWindow().mainloop()
        else:
            messagebox.showerror("Error", "No se pudo autenticar con Google.")
