import requests
import os
import sys
import json
from packaging import version

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
VERSION_FILE = os.path.join(BASE_DIR, "version.json")
UPDATE_URL = "https://raw.githubusercontent.com/fefedelcid/gym_manager/refs/heads/main/version.json"


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
        download_url = data["url"]

        # Comparar versiones
        if version.parse(latest_version) > version.parse(current_version):
            print(f"🚀 Nueva versión disponible: {latest_version}")
            update_app(download_url, latest_version)
        else:
            print("✅ La aplicación está actualizada.")

    except Exception as e:
        print(f"❌ Error al buscar actualizaciones: {e}")


def update_app(url, new_version):
    exe_name = sys.argv[0]
    new_exe = exe_name + ".new"

    print("⬇️ Descargando la nueva versión...")
    response = requests.get(url, stream=True)
    with open(new_exe, "wb") as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)

    print("🔄 Actualizando la aplicación...")

    backup_exe = exe_name + ".old"
    os.rename(exe_name, backup_exe) # Renombrar el ejecutable actual como respaldo
    os.rename(new_exe, exe_name) # Reemplazar con el nuevo ejecutable

    # 📌 Guardar la nueva versión en version.json
    with open(VERSION_FILE, "w") as f:
        json.dump({"version": new_version, "url": url}, f)

    print("🔁 Reiniciando la aplicación...")
    os.execv(exe_name, [exe_name])  # Reiniciar el programa

if __name__ == "__main__":
    check_for_updates()

