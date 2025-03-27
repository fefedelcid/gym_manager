import subprocess, os, sys
from src.config import VENV_PATH


def ensure_venv():
    """Crea un entorno virtual e instala dependencias si es necesario."""
    venv_dir = ".venv"

    if not os.path.exists(venv_dir):
        print("⚙️ Creando entorno virtual...")
        subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)

        print("📦 Instalando dependencias...")
        subprocess.run([VENV_PATH, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    return VENV_PATH

if __name__=="__main__":
    ensure_venv()
    print("Iniciando sistema...")
    subprocess.run([VENV_PATH, "main.py"])