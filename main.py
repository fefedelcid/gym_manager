from src.gui import MainWindow, LoginWindow
from src.services import get_google_credentials
from src.database import init_db
from src.core import sync_google_sheets, check_for_updates
from src.utils.logs_tracker import send_pending_log

import os
from src.config import REPO_PATH, LOGS_DIR
def move_existing_logs_to_folder():

    for filename in os.listdir(REPO_PATH):
        if filename.endswith(".log"):
            src = os.path.join(REPO_PATH, filename)
            dst = os.path.join(LOGS_DIR, filename)
            if not os.path.exists(dst):
                os.rename(src, dst)

def main():
    """Punto de entrada principal."""
    move_existing_logs_to_folder()
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