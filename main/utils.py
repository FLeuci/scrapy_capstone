import re
from datetime import datetime
import os
import yaml


class Configurations:
    def __init__(self, conf_path):
        with open(conf_path) as f:
            out_confs = yaml.load(f)
            self.gd_base_url = out_confs.get('gd_base_url')
            self.base_path = out_confs.get('base_path')
            self.base_path_empty = len(os.listdir(self.base_path)) == 0 if os.path.isdir(self.base_path) else True

confs = Configurations("/Users/scalabrese/PycharmProjects/scrapy_capstone/configurations/conf.yml")

def clean_records_regex(value):
    return re.sub(r"[\n\t\r]*", '', value) if value else None


def exec_func_chain(src_value, funcs):
    if (len(funcs) == 1):
        return funcs[0](src_value) if src_value else src_value
    else:
        return exec_func_chain(funcs[0](src_value) if src_value else src_value, funcs[1:])


def parse_dtts(date_str, src_format):
    return datetime.strptime(date_str, src_format).strftime('%Y%m%d') if date_str and src_format else None
