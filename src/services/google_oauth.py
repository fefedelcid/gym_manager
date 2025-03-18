import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

import sys

# Obtener la ruta del directorio raíz del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Agregar el directorio raíz al sys.path si no está ya presente
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)
from config.paths import CREDENTIALS_PATH, SCOPES, TOKEN_PATH


def get_google_credentials():
    """Autentica al usuario y devuelve las credenciales de Google OAuth."""
    creds = None

    # Cargar credenciales si existen
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, "rb") as token:
            creds = pickle.load(token)

    # Si no hay credenciales o están expiradas, autenticamos de nuevo
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)

        # Guardamos las credenciales para futuras ejecuciones
        with open(TOKEN_PATH, "wb") as token:
            pickle.dump(creds, token)

    return creds




if __name__ == "__main__":
    creds = get_google_credentials()
    print("Autenticación exitosa. Credenciales guardadas.")
