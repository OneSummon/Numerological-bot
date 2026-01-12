from datetime import datetime
from decimal import Decimal
import re

def is_valid_birth_date(date_str: str) -> bool:
    try:
        if len(date_str) != 10 or date_str[2] != '.' or date_str[5] != '.':
            return False
        
        parts = date_str.split('.')
        if len(parts) != 3:
            return False
        
        day, month, year = parts
        if not (day.isdigit() and month.isdigit() and year.isdigit()):
            return False
        
        day_int, month_int, year_int = int(day), int(month), int(year)
        
        current_year = datetime.now().year
        if not (1900 <= year_int <= current_year):
            return False
        if not (1 <= month_int <= 12):
            return False
        if not (1 <= day_int <= 31):
            return False
        
        datetime(year=year_int, month=month_int, day=day_int)
        
        return True
        
    except (ValueError, IndexError):
        return False

def is_valid_name(name_str: str) -> bool:
    try:
        if not (isinstance(name_str, str) and name_str.isalpha()):
            return False
        
        if len(name_str) < 2 or len(name_str) > 15:
            return False

        return True
    
    except (ValueError, IndexError):
        return False

def is_valid_username(username_str: str) -> bool:
    try:
        if not isinstance(username_str, str):
            return False
        
        if not username_str.startswith('@'):
            return False
        
        username_part = username_str[1:]
        
        if len(username_part) < 4 or len(username_part) > 32:
            return False
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username_part):
            return False
        
        if username_part[0].isdigit():
            return False
        
        if username_part.endswith('_'):
            return False
        
        if '__' in username_part:
            return False
        
        if not any(char.isalpha() for char in username_part):
            return False
        
        return True
    
    except (ValueError, IndexError, TypeError):
        return False
    
def is_valid_count_tokens(count_tokens: str) -> bool:
    try:
        if not isinstance(count_tokens, str):
            return False

        if not count_tokens.isdigit():
            return False
        
        if (Decimal(count_tokens) == 0) or (Decimal(count_tokens) < 0):
            return False

        return True
    except (ValueError, IndexError):
        return False