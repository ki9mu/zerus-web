# -*- coding: utf-8 -*-
# @Time : 2021/10/13 14:28
# @Author : ki9mu
# @File : poc.py
# @Software: PyCharm
import re


def poc_verify(response_data: str, response_header: dict, response_status: int, poc_res: dict) -> bool:
    # verify status code
    poc_status_list: list = poc_res.get("status_code")
    if response_status not in poc_status_list:
        return False

    # verify headers content
    poc_header_content_list = poc_res.get("header_list")
    if poc_header_content_list:
        header_key_list = list(response_header.keys())
        for poc_header_content in poc_header_content_list:
            if poc_header_content not in header_key_list:
                return False
    else:
        pass

    # verify headers re
    poc_header_re_list = poc_res.get("header_re")
    if poc_header_re_list:
        response_header_string = str(response_header)
        for poc_header_re in poc_header_re_list:
            result = re.findall(pattern=poc_header_re,string=response_header_string)
            if result:
                continue
            else:
                return False
    else:
        pass

    # verify content text
    poc_content_list = poc_res.get("content_list")
    if poc_content_list:
        for poc_content in poc_content_list:
            if poc_content not in response_data:
                return False
    else:
        pass

    # verify text re
    poc_content_re_list = poc_res.get("content_re")
    if poc_content_re_list:
        for poc_content_re in poc_content_re_list:
            result = re.findall(pattern=poc_content_re,string= response_data)
            if result:
                continue
            else:
                return False
    else:
        pass

    return True
