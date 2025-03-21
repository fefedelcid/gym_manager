import os
import pickle
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
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
        try:
            with open(TOKEN_PATH, "rb") as token:
                creds = pickle.load(token)
        except Exception as e:
            print(f"⚠️ Error al cargar token guardado: {e}")
            creds = None  # Invalida las credenciales si hay un error


    # Si no hay credenciales o están expiradas, autenticamos de nuevo
    if not creds or not creds.valid:
        try:
            if creds and creds.expired and creds.refresh_token:
                print("🔄 Token expirado. Intentando refrescar...")
                creds.refresh(Request())
                print("✅ Token refrescado con éxito.")
            else:
                print("🔑 No hay credenciales válidas. Solicitando autenticación...")
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
                creds = flow.run_local_server(port=0)
                print("✅ Autenticación completada.")

            # Guardamos las credenciales para futuras ejecuciones
            with open(TOKEN_PATH, "wb") as token:
                pickle.dump(creds, token)
        
        except RefreshError:
            print("❌ Error: Token expirado o revocado. Se requiere autenticación nuevamente.")
            os.remove(TOKEN_PATH)
            return get_google_credentials()  # Reintentar autenticación
        
        except Exception as e:
            print(f"❌ Error inesperado en la autenticación: {e}")
            return None  # Retorna None en caso de error

    return creds

if __name__ == "__main__":
    creds = get_google_credentials()
    if creds:
        print("✅ Autenticación exitosa.")
    else:
        print("❌ No se pudo autenticar.")
