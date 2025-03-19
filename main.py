import os
import sys
import subprocess
import traceback
from src.gui import MainWindow, LoginWindow
from src.services import get_google_credentials
from src.database import init_db
from src.core import sync_clients

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
    venv_dir = "venv"
    venv_python = os.path.join(venv_dir, "Scripts", "python.exe") if os.name == "nt" else os.path.join(venv_dir, "bin", "python")

    if not os.path.exists(venv_dir):
        print("⚙️ Creando entorno virtual...")
        subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)

    print("📦 Instalando dependencias...")
    subprocess.run([venv_python, "-m", "pip", "install", "-r", "requirements.txt"], check=True)

    return venv_python

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
    try:
        print("🔍 Verificando actualizaciones...")
        subprocess.run([sys.executable, "src/core/update.py"], check=True)

        venv_python = ensure_venv()
        subprocess.run([venv_python, "main.py"], check=True)

    except subprocess.CalledProcessError as e:
        error_message = f"⚠️ Error durante la ejecución: {e}\n"
        error_message += traceback.format_exc()

        if sys.stdout:  # Si hay consola, imprimir error
            print(error_message)
            print("Presiona Ctrl+C para salir o revisa la consola para depuración.")
            try:
                while True:
                    pass  # Espera indefinidamente hasta Ctrl+C
            except KeyboardInterrupt:
                print("\n👋 Saliendo del programa.")
        else:  # Si no hay consola, guardar error en un log
            with open("error.log", "w") as f:
                f.write(error_message)
