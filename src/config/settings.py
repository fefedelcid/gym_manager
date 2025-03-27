from os import path
import json

BASE_DIR = path.abspath(path.join(path.dirname(__file__), "../../"))

VERSION_FILE = path.join(BASE_DIR, "version.json")
data = "0.0.0"
with open(VERSION_FILE, "r") as f:
    data = json.load(f)["version"]

# Configuraciones ventana principal
WIDTH, HEIGHT = 1200, 600
APPEARANCE_MODE = "dark"
COLOR_THEME = "dark-blue"

TITLE = f"Gym Manager\t -\t v{data}"

# Configuración para google sheets
SPREADSHEET_NAME = "Formulario de Inscripción (Respuestas)"
REGISTRADOS = "Alumnos Registrados"
NUEVOS = "Respuestas de formulario 1"