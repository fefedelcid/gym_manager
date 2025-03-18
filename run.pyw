import os
import subprocess
import sys

# Verifica si se está ejecutando desde un ejecutable generado por PyInstaller
is_frozen = getattr(sys, 'frozen', False)

# Llamar a update.py antes de iniciar la app
print("Verificando actualizaciones...")
subprocess.run([sys.executable, "src/core/update.py"], check=True)

if is_frozen:
    # Si es un ejecutable (.exe), ejecuta directamente la app
    exe_path = os.path.join(os.path.dirname(sys.executable), "main.exe")
    print("Iniciando la aplicación desde el ejecutable...")
    subprocess.run([exe_path])
else:
    # Modo desarrollo: Ejecutar en entorno virtual si existe
    venv_dir = "venv"
    venv_python = os.path.join(venv_dir, "Scripts", "python.exe") if os.name == "nt" else os.path.join(venv_dir, "bin", "python")

    if not os.path.exists(venv_dir):
        print("Creando entorno virtual...")
        subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)

    print("Instalando dependencias...")
    subprocess.run([venv_python, "-m", "pip", "install", "-r", "requirements.txt"], check=True)

    print("Ejecutando la aplicación en modo desarrollo...")
    subprocess.run([venv_python, "main.py"], check=True)
