# -*- coding: utf-8 -*-
# @Time : 2021/6/30 17:14
# @Author : ki9mu
# @File : standard.py
# @Software: PyCharm
from typing import List


def fofa_standard(fofa_result: List) -> List:
    standard_url_list = []
    for url in fofa_result:
        if url[0][0:4] != "http":
            standard_url = "http://" + url[0]
        else:
            standard_url = url[0]
        standard_url_list.append(standard_url)
    return standard_url_list
