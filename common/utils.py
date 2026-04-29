import random
import string
from datetime import datetime, timedelta
from common.enums import Ccy
from common.constants import ISSUERS, NOTIONAL_MAX, NOTIONAL_MIN

def generate_trade_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

def generate_date(start_year=2020, end_year=2026):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    return start + timedelta(days=random.randint(0, (end - start).days))

def generate_notional(min_val=NOTIONAL_MIN, max_val=NOTIONAL_MAX):
    return random.uniform(min_val, max_val)

def generate_currency():
    return random.choice(list(Ccy))

def generate_issuer():
    return random.choice(ISSUERS)