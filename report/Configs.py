import re
from datetime import datetime

gd_base_url = "https://blog.griddynamics.com"


def clean_records_regex(value, downstream_func=lambda x: x):
    return downstream_func(re.sub(r"[\n\t\r]*", '', value)) if value else None


def pdtts(date_str, src_format):
    return datetime.strptime(date_str, src_format).strftime('%Y%m%d') if date_str and src_format else None
