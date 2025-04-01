from customtkinter import CTkFrame, CTkEntry
from datetime import datetime
from src.utils.helpers import _ensure_timezone

class EntryDate(CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self.day_entry = CTkEntry(self, width=35, justify="center", placeholder_text="DD")
        self.month_entry = CTkEntry(self, width=35, justify="center", placeholder_text="MM")
        self.year_entry = CTkEntry(self, width=60, justify="center", placeholder_text="AAAA")
        self.clear()

        self.day_entry.grid(row=0, column=0, padx=(0, 5))
        self.month_entry.grid(row=0, column=1, padx=(0, 5))
        self.year_entry.grid(row=0, column=2)
        
        self.day_entry.bind("<KeyRelease>", lambda e: self._move_focus(e, self.day_entry, self.month_entry, 2))
        self.month_entry.bind("<KeyRelease>", lambda e: self._move_focus(e, self.month_entry, self.year_entry, 2))
        self.year_entry.bind("<KeyRelease>", self._validate_year)
        
        for entry in [self.day_entry, self.month_entry, self.year_entry]:
            entry.bind("<KeyPress>", self._only_digits)
    
    def clear(self):
        self.day_entry.delete(0, 'end')
        self.month_entry.delete(0, 'end')
        self.year_entry.delete(0, 'end')
        
        self.day_entry.insert(0, f"{datetime.now().day:02}")
        self.month_entry.insert(0, f"{datetime.now().month:02}")
        self.year_entry.insert(0, f"{datetime.now().year}")

    def _only_digits(self, event):
        if not event.char.isdigit() and event.keysym not in ("BackSpace", "Tab", "Left", "Right"):
            return "break"
    
    def _move_focus(self, event, current, next_entry, limit):
        text = current.get()
        if len(text) >= limit:
            current.delete(limit, 'end')
            next_entry.focus_set()
    
    def _validate_year(self, event):
        text = self.year_entry.get()
        if len(text) > 4:
            self.year_entry.delete(4, 'end')
    
    def insert(self, value):
        if isinstance(value, str):
            try:
                date = datetime.strptime(value, "%d/%m/%Y")
            except ValueError:
                return
        elif isinstance(value, datetime):
            date = value
        else:
            return
        
        self.day_entry.delete(0, 'end')
        self.month_entry.delete(0, 'end')
        self.year_entry.delete(0, 'end')
        
        self.day_entry.insert(0, f"{date.day:02}")
        self.month_entry.insert(0, f"{date.month:02}")
        self.year_entry.insert(0, str(date.year))
    
    def get(self):
        try:
            day = int(self.day_entry.get())
            month = int(self.month_entry.get())
            year = int(self.year_entry.get())
            self.clear()
            return _ensure_timezone(datetime(year, month, day).date())
        except ValueError:
            return None