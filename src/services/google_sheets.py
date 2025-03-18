import os
import sys
# Obtener la ruta del directorio raíz del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Agregar el directorio raíz al sys.path si no está ya presente
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from src.services import get_google_credentials
from googleapiclient.discovery import build


def get_google_drive_service():
    """Autentica y devuelve un servicio de Google Drive API"""
    creds = get_google_credentials()
    service = build("drive", "v3", credentials=creds)
    return service


def get_google_sheets_service():
    """Autentica y devuelve un servicio de Google Sheets API"""
    creds = get_google_credentials()
    service = build("sheets", "v4", credentials=creds)
    return service


def find_spreadsheet(name):
    """Busca una hoja de cálculo en el Google Drive del usuario autenticado"""
    service = get_google_drive_service()
    query = f"name='{name}' and mimeType='application/vnd.google-apps.spreadsheet'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get("files", [])
    
    if files:
        return files[0]["id"]  # Retorna el ID de la hoja si existe
    return None


def read_sheet(spreadsheet_id, range_name, sheet):
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get("values", [])

    if not values:
        print("No se encontraron datos en la hoja.")
        return None
    else:
        return values


if __name__ == "__main__":
    SPREADSHEET_NAME = "Formulario de Inscripción (Respuestas)"
    id = find_spreadsheet(SPREADSHEET_NAME)
    service = get_google_sheets_service()
    sheet = service.spreadsheets()
    # read_sheet(id, "Respuestas de formulario 1", sheet)
    # read_sheet(id, "Alumnos Registrados", sheet)