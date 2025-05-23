from datetime import datetime, timezone, timedelta, date
from src.config import LOGS_DIR, LOCK_FILE
import os, inspect, sys


def remove_lock(*_):
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

def check_already_running():
    if os.path.exists(LOCK_FILE):
        print_log("Otra instancia ya está corriendo.")
        sys.exit(0)

    # Al cerrar la app, eliminamos el lock
    import atexit
    atexit.register(remove_lock)

    with open(LOCK_FILE, 'w') as f:
        f.write(str(os.getpid()))

def get_center(widget, width: float = 0, height: float = 0, w_hint: float = None, h_hint: float = None) -> str:
    '''
    Este método recibe un widget, ancho y alto, y opcionalmente factores de escala w_hint y h_hint.
    Luego, calcula la posición para que esté centrado en la pantalla.
    :return
    -> str()
    '''
    screen_width = widget.winfo_screenwidth()
    screen_height = widget.winfo_screenheight()
    
    # Si se proporcionan los hints, recalcular el tamaño
    if w_hint is not None:
        width = int(screen_width * w_hint)
    if h_hint is not None:
        height = int(screen_height * h_hint)
    
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    
    return f"{width}x{height}+{x}+{y-25}"

UTC_MINUS_3 = timezone(timedelta(hours=-3))

def _ensure_timezone(dt: datetime) -> datetime:
    """Asegura que el datetime tenga la zona horaria UTC-3 y lo convierte a UTC sin tzinfo."""
    try:
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=UTC_MINUS_3)
        else:
            dt = dt.astimezone(UTC_MINUS_3)
        return dt.astimezone(timezone.utc).replace(tzinfo=None)
    except AttributeError as e:
        print_log(f"[WARNING] on _ensure_timezone, exception: {e}")
        raise e

def get_timestamp() -> float:
    return _ensure_timezone(datetime.now()).timestamp()
SESSION_TIMESTAMP = datetime.fromtimestamp(get_timestamp())

# Inicializar archivo de logs
string = datetime.strftime(SESSION_TIMESTAMP, "%Y.%m.%d")
LOG_FILE = os.path.join(LOGS_DIR, f"{string}.log")

def print_log(message: str):
    """Escribe un mensaje en el archivo de logs con timestamp y contexto de llamada."""
    frame = inspect.currentframe()
    outer_frames = inspect.getouterframes(frame)

    # El índice 1 es quien llamó a `print_log`
    caller_frame = outer_frames[1]
    filename = caller_frame.filename.split("gym_manager")[1]
    lineno = caller_frame.lineno
    function = caller_frame.function

    # Intentar detectar la clase si estamos dentro de un método
    cls_name = None
    caller_locals = caller_frame.frame.f_locals
    if 'self' in caller_locals:
        cls_name = caller_locals['self'].__class__.__name__

    location = f"{filename}:"
    if cls_name:
        location += f"{cls_name}."
    location += f"{function}():{lineno}"

    timestamp = datetime.now(tz=UTC_MINUS_3).strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"|   [{timestamp}] [{location}] {message}\n"
    full_message = full_message.replace("|   ","|>>>") if "error" in full_message.lower() else full_message

    print(full_message)
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(full_message)

def init_logfile():
    timestamp = datetime.now(tz=UTC_MINUS_3).strftime("%Y-%m-%d %H:%M:%S")
    if os.path.isfile(LOG_FILE):
        with open(LOG_FILE, "a", encoding="utf-8") as file:
            file.write(f'|{">"*25} >>> >> >\n')
            file.write(f"|>>>[{timestamp}] [INFO] Nueva sesión iniciada.\n")
    else:
        with open(LOG_FILE, "w") as file:
            file.write(f"|   [{timestamp}] [INFO] Sistema inicializado.\n")

def parse_date(date_input) -> datetime:
    """Convierte una fecha en distintos formatos a un objeto datetime sin zona horaria."""
    # print_log(f"\n[INFO][parse_date] date_input:{date_input}, type:{type(date_input)}")
    
    if isinstance(date_input, datetime):  # Objeto datetime
        return _ensure_timezone(date_input)
    
    if isinstance(date_input, date):  # Objeto date
        return _ensure_timezone(datetime(date_input.year, date_input.month, date_input.day))

    if isinstance(date_input, (int, float)):  # Timestamp (segundos o milisegundos)
        return _parse_timestamp(date_input)

    if isinstance(date_input, str):  # Cadena de texto
        return _parse_string(date_input)

    if date_input == None:
        print_log(f"[WARNING] date_input type=<class 'NoneType'>")
        return ''

    raise ValueError(f"[ERROR] Formato de fecha no reconocido: {date_input}, type={type(date_input)}")

def _parse_timestamp(timestamp: float) -> datetime:
    """Convierte un timestamp (segundos o milisegundos) en un objeto datetime UTC sin tzinfo."""
    if timestamp > 10**10:  # Si es mayor a 10 dígitos, asumimos que está en milisegundos
        timestamp /= 1000
    dt = datetime.fromtimestamp(timestamp, tz=UTC_MINUS_3)
    return _ensure_timezone(dt)

def _parse_string(date_str: str) -> datetime:
    """Convierte una cadena de texto en un objeto datetime UTC sin tzinfo."""
    date_str = date_str.strip().split("+")[0]
    if date_str.isdecimal():
        return parse_date(int(date_str))

    date_formats = [
        "%d/%m/%Y",
        "%d/%m/%Y %H:%M:%S",
        "%m/%d/%Y %H:%M:%S",
        "%m/%d/%Y",
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S.%f"
        ]
    
    for fmt in date_formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return _ensure_timezone(dt)
        except ValueError:
            continue

    raise ValueError(f"[ERROR] Formato de fecha inválido: {date_str}, type={type(date_str)}")




