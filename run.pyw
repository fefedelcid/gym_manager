import subprocess, os, sys
from src.config import VENV_PATH
from src.utils import print_log, init_logfile, check_already_running


# check_already_running()

def ensure_venv():
    """Crea un entorno virtual e instala dependencias si es necesario."""
    venv_dir = ".venv"

    if not os.path.exists(venv_dir):
        print_log("⚙️ Creando entorno virtual...")
        subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)

        print_log("📦 Instalando dependencias...")
        subprocess.run([VENV_PATH, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    return VENV_PATH

if __name__=="__main__":
    ensure_venv()
    init_logfile()
    subprocess.run([VENV_PATH.replace("python", "pythonw"), "main.pyw"])