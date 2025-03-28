from src.utils import parse_date, UTC_MINUS_3
from datetime import timedelta, datetime
import re

def validate_phone(phone):
    """Valida un número de teléfono en formato internacional."""
    pattern = re.compile(r"^\+?[1-9]\d{1,14}$")
    return bool(pattern.match(phone))


def validate_email(email):
    """Valida un correo electrónico."""
    pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    return bool(pattern.match(email))


def validate_money(amount):
    """Valida un monto de dinero positivo con hasta dos decimales."""
    try:
        amount = float(amount)
        return amount >= 0 and round(amount, 2) == amount
    except ValueError:
        return False


def validate_date(date_input):
    """Verifica si una fecha es válida y retorna True/False."""
    try:
        parse_date(date_input)
        return True
    except ValueError:
        return False


def validate_text(text, min_length=1, max_length=255):
    """Valida un texto con longitud dentro de un rango específico."""
    return isinstance(text, str) and min_length <= len(text.strip()) <= max_length

def get_tag(cliente) -> tuple[str, ...]:
    DAYS_30 = timedelta(days=30)
    DAYS_15 = timedelta(days=15)
    TODAY = datetime.now(tz=UTC_MINUS_3)
    
    if cliente.lastPayment is None or cliente.needCheck:
        return ("need_check", )
    
    # Asegurar que cliente.lastPayment tenga la misma zona horaria
    lastPayment = cliente.lastPayment
    if lastPayment.tzinfo is None:
        lastPayment = lastPayment.replace(tzinfo=UTC_MINUS_3)

    time_diff = TODAY - lastPayment
    if time_diff > DAYS_30:
        return ("expired", )
    elif time_diff > DAYS_15:
        return ("to_expire", )
    return ("", )