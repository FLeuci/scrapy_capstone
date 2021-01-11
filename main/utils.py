import json
import re
from datetime import datetime
import os
import yaml
import pandas as pd

with open("conf.yml") as f:
    confs = yaml.safe_load(f)
gd_base_url = confs.get("gd_base_url")
base_path = confs.get(os.path.dirname(__file__)) + "/data"

base_path_empty = len(os.listdir(__file__)) == 0 if os.path.isdir(__file__) else True


def clean_records_regex(value):
    """
    Remove '\n\t\r' representing tabs and newlines from an extracted data
    """
    return re.sub(r"[\n\t\r]*", '', value) if value else None


def exec_func_chain(src_value, funcs):
    """
    Execute all the functions inside funcs in a head-tail fashioned recursively
    :param src_value: input of the head function
    :param funcs: all the following functions
    :return: result of the function chain
    """
    if len(funcs) == 1:
        return funcs[0](src_value) if src_value else src_value
    else:
        return exec_func_chain(funcs[0](src_value) if src_value else src_value, funcs[1:])


def parse_dtts(date_str, src_format):
    """
    Parse a date with the needed format and convert it to timestamp
    """
    return datetime.strptime(date_str, src_format).strftime('%Y%m%d') if date_str and src_format else None


def flatten(list_of_list, func):
    """
    Flats a list of lists in one unique list
    """
    from functools import reduce
    return reduce(lambda accumulator, combiner: accumulator + list(map(func, combiner)), list_of_list, list())


def count_by_key(list_of_tuple_2):
    """
    Groups key-value list in a dict which contains unique key with the count of occurrences
    :param list_of_tuple_2: key-list(values)
    :return: dict of key-count of values
    """
    res = dict()
    for tuple_2 in list_of_tuple_2:
        if res.__contains__(tuple_2[0]):
            res.update({tuple_2[0]: res[tuple_2[0]] + 1})
        else:
            res.update({tuple_2[0]: 1})
    return res

def write_in_data(path, content):
    """
    Fai funzione che che salva in main/data
    """
    with open(f"{base_path}/{path}", "w") as f:
        f.write(content)

def read_from_data(path):
    """
    Fai funzione che che legge json da main/data
    """
    pd.read_json(f'{base_path}/{path}')
