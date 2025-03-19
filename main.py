import os
import sys
from subprocess import run
from src.gui import MainWindow, LoginWindow
from src.services import get_google_credentials
from src.database import init_db
from src.core import sync_clients, check_for_updates
from src.config import VENV_PATH

def sync_google_sheets():
    """Ejecuta la sincronización con Google Sheets en un hilo separado."""
    try:
        print("🔄 Iniciando sincronización con Google Sheets...")
        sync_clients()
        print("✅ Sincronización completada.")
    except Exception as e:
        print(f"❌ Error durante la sincronización: {e} {type(e)}")

def ensure_venv():
    """Crea un entorno virtual e instala dependencias si es necesario."""
    venv_dir = ".venv"

    if not os.path.exists(venv_dir):
        print("⚙️ Creando entorno virtual...")
        run([sys.executable, "-m", "venv", venv_dir], check=True)

        print("📦 Instalando dependencias...")
        run([VENV_PATH, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    return VENV_PATH

def main():
    """Punto de entrada principal."""
    init_db()
    creds = get_google_credentials()

    if creds:
        sync_google_sheets()
        MainWindow().mainloop()
    else:
        LoginWindow().mainloop()

if __name__ == "__main__":
    check_for_updates()

    if sys.prefix != os.path.abspath(".venv"):
        run([ensure_venv(), os.path.abspath(__file__)])
    else:
        main()