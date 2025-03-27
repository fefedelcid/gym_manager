from src.gui import MainWindow, LoginWindow
from src.services import get_google_credentials
from src.database import init_db
from src.core import sync_google_sheets, check_for_updates


def main():
    """Punto de entrada principal."""
    init_db()
    creds = get_google_credentials()

    if creds:
        sync_google_sheets()
        MainWindow().mainloop()
    else:
        LoginWindow().mainloop()


if __name__ == "__main__":
    check_for_updates()
    main()