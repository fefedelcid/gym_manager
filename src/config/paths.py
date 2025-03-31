import os

# Directorio base del proyecto (src)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_PATH = os.path.join(BASE_DIR, "../")
VENV_PATH = os.path.join(".venv", "Scripts", "python.exe") if os.name == "nt" else os.path.join(".venv", "bin", "python")


# Rutas importantes
CONFIG_DIR = os.path.join(BASE_DIR, "config")
SESSION_DIR = os.path.join(BASE_DIR, "core/session")
VERSION_FILE = os.path.join(BASE_DIR, "../version.json")
SECRETS_DIR = os.path.join(CONFIG_DIR, "secrets")
CREDENTIALS_PATH = os.path.join(SECRETS_DIR, "credentials.json")

# Ruta para guardar las credenciales autenticadas
TOKEN_PATH = os.path.join(os.path.dirname(CREDENTIALS_PATH), "token.pickle")

# Ruta de version.json (remoto)
UPDATE_URL = "https://raw.githubusercontent.com/fefedelcid/gym_manager/refs/heads/main/version.json"


# Verificación de existencia de credenciales
if not os.path.exists(CREDENTIALS_PATH):
    raise FileNotFoundError(f"El archivo de credenciales no se encuentra en {CREDENTIALS_PATH}")
if not os.path.exists(SESSION_DIR):
    os.mkdir(SESSION_DIR)

# Alcance de la app
SCOPES = [
    # "https://www.googleapis.com/auth/forms.body",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.metadata.readonly"
]