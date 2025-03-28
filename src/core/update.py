import requests
import os, sys, json
import subprocess
from packaging import version
from src.config import VERSION_FILE, UPDATE_URL, REPO_PATH
from src.utils import print_log


def get_current_version():
    try:
        with open(VERSION_FILE, "r") as f:
            data = json.load(f)
            return data["version"]
    except FileNotFoundError:
        return "0.0.0"
    except Exception as e:
        print_log(f"Error al leer version.json: {e}")
        return "0.0.0"


def check_for_updates():
    try:
        print_log("🔍 Buscando actualizaciones...")

        # Obtener versión instalada
        current_version = get_current_version()

        # Obtener última versión de GitHub
        response = requests.get(UPDATE_URL)
        response.raise_for_status() # Si hay un error HTTP, lanza una excepción
        latest = response.json()["version"]

        # Comparar versiones
        if version.parse(latest) > version.parse(current_version):
            print_log(f"🚀 Nueva versión disponible: {latest}")
            update_app(current_version, latest)
        else:
            print_log(f"✅ La aplicación está actualizada. {current_version} / {latest}")

    except Exception as e:
        print_log(f"❌ Error al buscar actualizaciones: {e}")


def update_app(current, latest):
    if not os.path.exists(os.path.join(REPO_PATH, ".git")):
        print_log("❌ No es un repositorio git. No se pueden aplicar actualizaciones.")
        return

    # Intento hacer pull para actualizar solo los archivos modificados
    try:
        print_log(f"🔄 Actualizando v{current} a v{latest}...")
        subprocess.run(["git", "fetch", "--all"], cwd=REPO_PATH, check=True)
        subprocess.run(["git", "reset", "--hard", "origin/main"], cwd=REPO_PATH, check=True)
        print_log("✅ Sistema actualizado con éxito.")
        
        # Reiniciar la aplicación
        print_log("🔄 Reiniciando la aplicación...")
        os.execv(sys.executable, "python", sys.argv)
    except subprocess.CalledProcessError as e:
        print_log(f"❌ Error al actualizar: {e}")


if __name__ == "__main__":
    check_for_updates()

