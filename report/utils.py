import re
from datetime import datetime
import os

gd_base_url = "https://blog.griddynamics.com"
base_path = "./data/"


def clean_records_regex(value, downstream_func=lambda x: x):
    return downstream_func(re.sub(r"[\n\t\r]*", '', value)) if value else None


def parse_dtts(date_str, src_format):
    return datetime.strptime(date_str, src_format).strftime('%Y%m%d') if date_str and src_format else None


base_path_empty = len(os.listdir(base_path)) == 0 if os.path.isdir(base_path) else True
