from src.gui import MainWindow, LoginWindow
from src.services import get_google_credentials
from src.database import init_db
from src.core import sync_clients

def sync_google_sheets():
    """Ejecuta la sincronización con Google Sheets en un hilo separado."""
    try:
        print("🔄 Iniciando sincronización con Google Sheets...")
        sync_clients()  # Ahora llamamos directamente a la función
        print("✅ Sincronización completada.")
    except Exception as e:
        print(f"❌ Error durante la sincronización: {e} {type(e)}")


if __name__ == "__main__":
    init_db()
    creds = get_google_credentials()

    if creds:
        # Ejecutar sincronización
        sync_google_sheets()

        # Iniciar ventana principal
        MainWindow().mainloop()
    else:
        LoginWindow().mainloop()
