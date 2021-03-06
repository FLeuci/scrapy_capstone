import json
import re
from datetime import datetime
import os
import pandas as pd
import subprocess

gd_base_url = "https://blog.griddynamics.com"
base_path = os.path.dirname(__file__) + "/data"
if not os.path.exists(base_path):
    os.mkdir(base_path)


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


def write_data_append(path, content):
    """
    Appends in main/data
    """
    with open(f"{base_path}/{path}", "a") as f:
        f.write(content + "\n")


def write_in_data(path, content):
    """
    Saves in main/data
    """
    with open(f"{base_path}/{path}", "w") as f:
        f.write(content)


def read_from_data(path, is_pandas=False):
    """
    Reads-buffer from main/data
    """
    if is_pandas and path_exist(path):
        return pd.read_json(f"{base_path}/{path}", lines=True)
    elif path_exist(path):
        with open(f'{base_path}/{path}', 'rb') as f:
            data = f.readlines()
        data = list(map(lambda x: x.rstrip().decode("utf-8"), data))
        data_json_str = "[" + ','.join(data) + "]"
        return json.loads(data_json_str)
    else:
        return {}


def drop_data_file_if_exists(path):
    """
    Deletes content from a file if not empty
    """
    if os.path.exists(f'{base_path}/{path}'):
        os.remove(f'{base_path}/{path}')


def path_exist(path):
    """
    Returns True if a file exists
    """
    return os.path.isfile(f'{base_path}/{path}')


def exec_spider(spider_name):
    """
    Runs a spider using subprocesses
    """
    process = subprocess.run(['scrapy', 'crawl', spider_name], check=True, stdout=subprocess.PIPE,
                             universal_newlines=True)
    output = process.stdout
    print(output)


crawl_date = read_from_data('crawl_checkpoint.json') \
             or [{'LastExecutionDate': '19900101', 'LastExecutionArticleNum': 0}]
