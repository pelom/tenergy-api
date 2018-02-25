import json
import datetime
import pytz
import logging

import os

script_dir = os.path.dirname(__file__)
rel_path = "config.json"
abs_file_path = os.path.join(script_dir, rel_path)

print abs_file_path

config = None
with open(abs_file_path) as json_data_file:
    config = json.load(json_data_file)


def log(class_name):
    log_config = config.get('log')
    logger = logging.getLogger(class_name)
    logger.setLevel(log_config.get('level'))

    formatter = logging.Formatter(log_config.get('formatter'))

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_config.get('level'))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if log_config.get('outputfile') is True:
        file_handler = logging.FileHandler(log_config.get('filepath'), encoding="UTF-8")
        file_handler.setLevel(log_config.get('level'))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def datetime_now_tz():
    dat = datetime.datetime.now(tz=pytz.timezone(config.get('timezone')))
    return dat
