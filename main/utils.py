import re
from datetime import datetime
import os

gd_base_url = "https://blog.griddynamics.com"
base_path = "/Users/fleuci/report/data/"


def clean_records_regex(value):
    return re.sub(r"[\n\t\r]*", '', value) if value else None


def exec_func_chain(src_value, funcs):
    if (len(funcs) == 1):
        return funcs[0](src_value) if src_value else src_value
    else:
        return exec_func_chain(funcs[0](src_value) if src_value else src_value, funcs[1:])


def parse_dtts(date_str, src_format):
    return datetime.strptime(date_str, src_format).strftime('%Y%m%d') if date_str and src_format else None


def flatten(list_of_list, func):
    from functools import reduce
    return reduce(lambda accumulator, combiner: accumulator + list(map(func, combiner)), list_of_list, list())

def reduce_by_key(list_of_tuple_2):
    res = dict()
    for tuple_2 in list_of_tuple_2:
        if res.__contains__(tuple_2[0]):
            res.update({tuple_2[0]: res[tuple_2[0]] + 1})
        else:
            res.update({tuple_2[0]: 1})
    return res

base_path_empty = len(os.listdir(base_path)) == 0 if os.path.isdir(base_path) else True
