import requests
import os, sys, json
import subprocess
from packaging import version
from src.config import VERSION_FILE, UPDATE_URL, REPO_PATH


def get_current_version():
    try:
        with open(VERSION_FILE, "r") as f:
            data = json.load(f)
            return data["version"]
    except FileNotFoundError:
        return "0.0.0"
    except Exception as e:
        print(f"Error al leer version.json: {e}")
        return "0.0.0"


def check_for_updates():
    try:
        print("🔍 Buscando actualizaciones...")

        # Obtener versión instalada
        current_version = get_current_version()

        # Obtener última versión de GitHub
        response = requests.get(UPDATE_URL)
        response.raise_for_status() # Si hay un error HTTP, lanza una excepción
        data = response.json()
        
        latest_version = data["version"]

        # Comparar versiones
        if version.parse(latest_version) > version.parse(current_version):
            print(f"🚀 Nueva versión disponible: {latest_version}")
            update_app()
        else:
            print("✅ La aplicación está actualizada.")

    except Exception as e:
        print(f"❌ Error al buscar actualizaciones: {e}")


def update_app():
    if not os.path.exists(os.path.join(REPO_PATH, ".git")):
        print("❌ No es un repositorio git. No se pueden aplicar actualizaciones.")
        return

    # Intento hacer pull para actualizar solo los archivos modificados
    try:
        print("🔄 Buscando actualizaciones...")
        subprocess.run(["git", "pull", "origin", "main"], cwd=REPO_PATH, check=True)
        print("✅ Aplicadas actualizaciones con éxito.")
        
        # Reiniciar la aplicación
        print("🔄 Reiniciando la aplicación...")
        os.execv(sys.executable, [sys.executable] + sys.argv)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al actualizar: {e}")


if __name__ == "__main__":
    check_for_updates()

