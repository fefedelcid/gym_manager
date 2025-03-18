import os

# Directorio base del proyecto (src)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Rutas importantes
CONFIG_DIR = os.path.join(BASE_DIR, "config")
SECRETS_DIR = os.path.join(CONFIG_DIR, "secrets")
CREDENTIALS_PATH = os.path.join(SECRETS_DIR, "credentials.json")

# Ruta para guardar las credenciales autenticadas
TOKEN_PATH = os.path.join(os.path.dirname(CREDENTIALS_PATH), "token.pickle")

# Verificación de existencia de credenciales
if not os.path.exists(CREDENTIALS_PATH):
    raise FileNotFoundError(f"El archivo de credenciales no se encuentra en {CREDENTIALS_PATH}")


# Alcance de la app
SCOPES = [
    # "https://www.googleapis.com/auth/forms.body",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.metadata.readonly"
]