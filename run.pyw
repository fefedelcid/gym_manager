import subprocess, os, sys
from src.config import VENV_PATH
from src.utils import print_log

def normalize_package_name(name):
    """Normaliza el nombre del paquete reemplazando guiones por guiones bajos."""
    return name.replace('-', '_').lower()

def get_installed_packages():
    """Obtiene el listado de paquetes instalados."""
    output = subprocess.check_output([VENV_PATH, "-m", "pip", "freeze"], text=True)
    return {normalize_package_name(line.split("==")[0]) for line in output.strip().split("\n") if "==" in line}

def get_required_packages():
    """Obtiene el listado de paquetes requeridos del archivo requirements.txt."""
    with open("requirements.txt", "r") as req_file:
        return {normalize_package_name(line.strip().split("==")[0]) for line in req_file if line.strip() and not line.startswith('#')}

def check_dependencies():
    """Verifica si todas las dependencias en requirements.txt están instaladas."""
    try:
        installed = get_installed_packages()
        required = get_required_packages()

        missing = required - installed
        if missing:
            print_log(f"\u26A0\uFE0F Faltan dependencias: {', '.join(missing)}. Instalando...")
            subprocess.run([VENV_PATH, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        else:
            print_log("\u2705 Todas las dependencias están instaladas.")
    except Exception as e:
        print_log(f"Error verificando dependencias: {e}")


def ensure_venv():
    """Crea un entorno virtual e instala dependencias si es necesario."""
    venv_dir = ".venv"

    if not os.path.exists(venv_dir):
        print_log("⚙️ Creando entorno virtual...")
        subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)

        print_log("📦 Instalando dependencias...")
        subprocess.run([VENV_PATH, "-m", "pip", "install", "-r", "requirements.txt"], check=True)

    check_dependencies()
    return VENV_PATH

if __name__=="__main__":
    # check_dependencies()
    ensure_venv()
    print_log("Iniciando sistema...")
    subprocess.run([VENV_PATH, "main.py"])