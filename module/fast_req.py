# -*- coding: utf-8 -*-
# @Time   : 2021/10/12 2:19 下午
# @Author : ki9mu
# @File   : fast_req.py
import aiohttp
import asyncio
import time
from utils.poc import poc_verify
from utils.read_file import *


async def fast_req(url, poc_dict):
    if "http" not in url:
        url = "http://" + url
    req: dict = poc_dict.get("request")
    res: dict = poc_dict.get("response")
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        path: str = req.get("path")
        method: str = req.get("method")
        data: str = req.get("data")
        header: dict = req.get("header")
        if path != "/":
            url = url + path
        async with session.request(url=url, method=method, data=data, headers=header) as response:
            assert response.status
            res_data = await response.text()
            res_headers = dict(response.headers)
            res_status = response.status
            if poc_verify(response_data=res_data, response_header=res_headers, response_status=res_status, poc_res=res):
                print(url)
            else:
                pass


class FastRequests:
    def __init__(self, url_list: list, poc_dict):
        self.res_template = {
            "type": "{type_info}",
            "code": "{type_code}",
            "error_log": "{error_log}",
            "info": {}
        }
        self.url_list = url_list
        self.poc_dict = poc_dict

    def init(self):
        # detect url list
        for url in self.url_list:
            if "http" not in url:
                self.res_template.get("type").format(type_info="error")
                self.res_template.get("code").format(type_code="1")
                self.res_template.get("error_log").format(error_log="requests list illegal")
                return self.res_template

        # detect poc
        self.poc_dict: dict = poc_dict
        pass

    def start(self):
        start_time = time.time()
        task_list = []
        asyncio.Semaphore = 500
        loop = asyncio.get_event_loop()

        # temp
        poc_dict = self.poc_dict.get("attack")[0]
        print(poc_dict)

        for url in self.url_list:
            task_list.append(asyncio.ensure_future(fast_req(url, poc_dict=poc_dict)))
        loop.run_until_complete(asyncio.wait(task_list))

        end_time = time.time()
        run_time = end_time - start_time
        print(run_time)


if __name__ == '__main__':
    poc_dict = read_yaml("../poc/django_debug_mode.yaml")
    print(poc_dict)
    url_list = ["http://ifs.yimidida.com:8080"]
    f_req = FastRequests(url_list=url_list, poc_dict=poc_dict)
    f_req.start()
