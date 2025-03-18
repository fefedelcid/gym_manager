from customtkinter import CTkFrame, CTkEntry
import re


class MoneyEntry(CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self.entry = CTkEntry(self, justify="right")
        self.entry.pack(fill="both", expand=True)
        
        self.entry.bind("<KeyPress>", self._only_valid_chars)
        self.entry.bind("<FocusOut>", self._format_money)
    
    def clear(self):
        self.entry.delete(0, 'end')

    def _only_valid_chars(self, event):
        valid_chars = "0123456789.,$"
        if event.char and event.char not in valid_chars and event.keysym not in ("BackSpace", "Left", "Right", "Tab"):
            return "break"
    
    def _format_money(self, event=None):
        text = self.entry.get()
        text = re.sub(r"[^0-9,.]", "", text)  # Elimina cualquier carácter que no sea número, punto o coma
        
        if "," in text and "." in text:
            if text.rfind(",") > text.rfind("."):
                text = text.replace(".", "")  # Formato con punto como separador de miles
            else:
                text = text.replace(",", "")  # Formato con coma como separador de miles
        
        text = text.replace(",", ".")  # Asegurar que solo se use punto decimal
        
        try:
            value = float(text)
            self.entry.delete(0, 'end')
            self.entry.insert(0, f"${value:,.2f}")
        except ValueError:
            self.entry.delete(0, 'end')
    
    def get(self):
        text = self.entry.get()
        text = re.sub(r"[^0-9.]", "", text)  # Elimina símbolos y separadores de miles
        try:
            return float(text)
        except ValueError:
            return None
