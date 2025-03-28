import subprocess, os, sys
from src.config import VENV_PATH
from src.utils import print_log


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
    print_log("Iniciando sistema...")
    subprocess.run([VENV_PATH, "main.py"])