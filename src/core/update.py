import requests
import os
import sys
import json

VERSION = "1.0.0"
UPDATE_URL = "https://raw.githubusercontent.com/fefedelcid/gym_manager/refs/heads/main/version.json"

import requests
import os
import sys
import json

VERSION = "1.0.0"
UPDATE_URL = "https://raw.githubusercontent.com/usuario/MiApp/main/version.json"

def check_for_updates():
    try:
        response = requests.get(UPDATE_URL)
        data = response.json()
        latest_version = data["version"]
        download_url = data["url"]

        if latest_version > VERSION:
            print(f"Nueva versión disponible: {latest_version}")
            update_app(download_url)
        else:
            print("La aplicación está actualizada.")

    except Exception as e:
        print(f"Error al buscar actualizaciones: {e}")

def update_app(url):
    response = requests.get(url, stream=True)
    with open("MiApp_new.exe", "wb") as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)

    os.replace("MiApp_new.exe", sys.argv[0])
    os.execl(sys.argv[0], sys.argv[0])  # Reinicia la app

if __name__ == "__main__":
    check_for_updates()

