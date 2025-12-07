import re

def normalize_phone(phone: str) -> str:
    """
    Простая нормализация: оставить только цифры и ведущий '+' если есть.
    """
    phone = phone.strip()
    plus = '+' if phone.startswith('+') else ''
    digits = re.sub(r'\D', '', phone)
    return plus + digits
