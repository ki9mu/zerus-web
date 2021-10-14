# -*- coding: utf-8 -*-
# @Time : 2021/10/13 14:27
# @Author : ki9mu
# @File : read_file.py
# @Software: PyCharm
import yaml


def read_yaml(yaml_path: str) -> dict:
    with open(yaml_path, 'r', encoding="utf8") as f:
        poc_dict = yaml.safe_load(f)
    return poc_dict
