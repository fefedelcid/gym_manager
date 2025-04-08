import os, json
from datetime import timedelta, datetime
from src.config import LOGS_DIR
from src.utils.helpers import SESSION_TIMESTAMP, print_log, _ensure_timezone
from src.services import send_email_with_attachments, get_google_credentials

SENT_LOGS_TRACKER = os.path.join(LOGS_DIR, "sent_logs.json")
LAST_SEND_FILE = os.path.join(LOGS_DIR, "timestamp.json")


def was_log_sent(log_filename):
    if not os.path.exists(SENT_LOGS_TRACKER):
        return False
    with open(SENT_LOGS_TRACKER, "r", encoding="utf-8") as f:
        sent = json.load(f)
    return log_filename in sent


def mark_log_as_sent(log_filename):
    sent = []
    if os.path.exists(SENT_LOGS_TRACKER):
        with open(SENT_LOGS_TRACKER, "r", encoding="utf-8") as f:
            sent = json.load(f)
    sent.append(log_filename)
    with open(SENT_LOGS_TRACKER, "w", encoding="utf-8") as f:
        json.dump(sent, f, indent=2)

def send_pending_log():
    print_log("[INFO] Iniciando proceso de envío de logs pendientes...")

    # Construir lista de logs ordenada por fecha descendente
    log_files = sorted(
        [f for f in os.listdir(LOGS_DIR) if f.endswith(".log")],
        key=lambda name: datetime.strptime(name.replace(".log", ""), "%Y.%m.%d"),
        reverse=True
    )

    # Calcular la fecha de ayer
    yesterday = SESSION_TIMESTAMP - timedelta(days=1)
    yesterday_str = yesterday.strftime("%Y.%m.%d")

    # Buscar el índice del log de ayer en la lista
    target_index = next((i for i, f in enumerate(log_files) if f.startswith(yesterday_str)), None)
    if target_index is None:
        print_log("[INFO] No se encontró el log de ayer. Buscando el más reciente anterior...")
        # Buscar el log más reciente anterior al de ayer
        for log_file in log_files:
            log_date = datetime.strptime(log_file.replace(".log", ""), "%Y.%m.%d")
            if log_date < yesterday:
                if not was_log_sent(log_file):
                    _send_log_file(log_file, "[📘] Envío automático de log anterior al de ayer")
                    return
                else:
                    print_log(f"[INFO] El log {log_file} ya fue enviado.")
                    return
        print_log("[INFO] No se encontró ningún log anterior pendiente de envío.")
        return

    # Si encontramos el log de ayer
    log_file = log_files[target_index]
    if not was_log_sent(log_file):
        _send_log_file(log_file, "[📘] Envío automático del log de ayer")
    else:
        print_log("[INFO] El log de ayer ya fue enviado. No se enviará nada.")
    

# comando para enviar log de hoy con cd de 1hs
def can_send_today_log():
    if not os.path.exists(LAST_SEND_FILE):
        return True
    with open(LAST_SEND_FILE, "r") as f:
        data = json.load(f)
    last_ts = datetime.fromisoformat(data["timestamp"])
    cd = _ensure_timezone(datetime.now()) - last_ts
    return cd >= timedelta(hours=1)

def update_last_send_timestamp():
    with open(LAST_SEND_FILE, "w") as f:
        json.dump({"timestamp": _ensure_timezone(datetime.now()).isoformat()}, f)

def send_today_log():
    if not can_send_today_log():
        print_log("[WARNING] ⏳ Debe esperar una hora antes de volver a enviar el log de hoy.")
        return False

    log_name = f"{SESSION_TIMESTAMP.strftime('%Y.%m.%d')}.log"
    log_path = os.path.join(LOGS_DIR, log_name)

    if os.path.exists(log_path):
        if _send_log_file(log_name, "📘 Log del día (envío manual)"):
            update_last_send_timestamp()


def _send_log_file(log_filename: str, subject: str):
    log_path = os.path.join(LOGS_DIR, log_filename)
    log_date_str = log_filename.replace(".log", "")
    print_log(f"[INFO] Enviando log: {log_filename}")
    
    success = send_email_with_attachments(
        get_google_credentials(),
        to_email="fdelcid.dev@gmail.com",
        subject=subject,
        body_text=f"Log generado el día {log_date_str}",
        attachments=[log_path]
    )
    if success:
        mark_log_as_sent(log_filename)
        print_log("[SUCCESS] Log enviado con éxito.")
        return True
    else:
        print_log("[ERROR] No se pudo enviar el log.")
        return False