import os
import subprocess
import sys

# Ruta al directorio del entorno virtual
venv_dir = "venv"

# Ruta al ejecutable de Python dentro del entorno virtual
venv_python = os.path.join(venv_dir, "Scripts", "python.exe") if os.name == "nt" else os.path.join(venv_dir, "bin", "python")

# Verifica si el entorno virtual no existe
if not os.path.exists(venv_dir):
    # Intenta importar virtualenv, si falla, lo instala
    try:
        import virtualenv # type: ignore
    except ImportError:
        print("virtualenv no está instalado. Instalando...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "virtualenv"])
        # if os.name == "nt":
        # else:
        #     subprocess.check_call([sys.executable, "-m", "pip3", "install", "virtualenv"])
    
    # Crea el entorno virtual
    print("Creando entorno virtual...")
    subprocess.check_call([sys.executable, "-m", "virtualenv", venv_dir])

# Instala las dependencias en el entorno virtual
print("Instalando dependencias...")
subprocess.check_call([venv_python, "-m", "pip", "install", "-r", "requirements.txt"])

# Ejecuta el archivo main.py dentro del entorno virtual
print("Ejecutando la aplicación...")
os.execv(venv_python.replace("python", "pythonw"), ["python", "main.py"])
