from src.gui import MainWindow, LoginWindow
from src.services import get_google_credentials
from src.database import init_db
from src.core import sync_google_sheets, check_for_updates
from src.utils.logs_tracker import send_pending_log


def main():
    """Punto de entrada principal."""
    init_db()
    creds = get_google_credentials()

    if creds:
        send_pending_log()
        sync_google_sheets()
        MainWindow().mainloop()
    else:
        LoginWindow().mainloop()


if __name__ == "__main__":
    check_for_updates()
    main()