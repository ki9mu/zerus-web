# -*- coding: utf-8 -*-
# @Time : 2021/3/23 13:57
# @Author : ki9mu
# @File : Get_FOFA.py
# @Software: PyCharm
from typing import Dict, List

import requests


class GetFOFA:
    def __init__(self, email, key):
        self.email = email
        self.key = key
        self.auth_url = "https://fofa.so/api/v1/info/my?email={email}&key={key}"
        self.query_url = "https://fofa.so/api/v1/search/all?email={email}&key={key}&qbase64={qbase64}&size={size}"
        self.error = False
        # 如果认证出错，后面的函数都返回空
        res_result = requests.get(self.auth_url.format(email=self.email, key=self.key))
        if res_result.json().get("error"):
            self.error = True

    def query(self, query: str, size: int = 9999) -> list:
        if self.error:
            return []

        from base64 import b64encode
        query_base64 = b64encode(query.encode()).decode()
        query_data: Dict = requests.get(
            self.query_url.format(email=self.email, key=self.key, qbase64=query_base64, size=size)
        ).json()
        return query_data.get("results")

    def big_china_query(self, query: str) -> [List, Dict, List]:
        """
        获取输入数据，尽可能获取全国各地的数据，若国内总数小于9999，默认使用国内数据
        :param query: fofa语句
        :return: list表单 格式如[[ip:port,ip,port]]
        """
        if self.error:
            return []

        # 如果本身国内总数少于9999的话，直接使用默认的
        query_str = "{query} && country = \"CN\"".format(query=query)
        default_query = self.query(query_str, size=9999)
        if len(default_query) < 9999:
            return default_query
        else:
            # 遍历每个省份
            region_list = ['region="" && country="CN"', 'region="Guangdong"', 'region="Shandong"', 'region="Shanghai"',
                           'region="Beijing"',
                           'region="Zhejiang"', 'region="Jiangsu"', 'region="Henan"', 'region="Fujian"',
                           'region="Sichuan"',
                           'region="Chongqing"', 'region="Hunan"', 'region="Hubei"', 'region="Shaanxi"',
                           'region="Liaoning"', 'region="Tianjin"', 'region="Anhui"', 'region="Hebei"',
                           'region="Jiangxi"',
                           'region="Guangxi"', 'region="Yunnan"', 'region="Shanxi"', 'region="Jilin"',
                           'region="Guizhou"',
                           'region="Ningxia Hui Autonomous Region"', 'region="Heilongjiang"', 'region="Hainan"',
                           'region="Gansu"', 'region="Inner Mongolia Autonomous Region"', 'region="Qinghai"',
                           'region="Xinjiang"', 'region="Tibet"']
            data = []
            for region in region_list:
                regio_query = "{query} && {region}".format(query=query, region=region)
                query_data = self.query(query=regio_query, size=9999)
                # print(query_data)
                # 如果响应未出错
                data = data + query_data

            set_data: List = []
            for url in data:
                if url not in set_data:
                    set_data.append(url)
            return set_data

    def biggest_query(self, query: str) -> List:
        """
        :param query: fofa语句
        :return: 返回list
        """
        if self.error:
            return []
        # 如果全世界总数少于9999的话，直接使用默认的
        default_query = self.query(query=query, size=9999)
        if len(default_query) < 9999:
            return default_query

        # 尽最大可能获取全世界所有
        country_list = ["AL", "DZ", "AF", "AR", "AZ", "AE", "AW", "OM", "EG", "ET", "IE", "EE", "AD", "AO", "AI", "AG",
                        "AT", "AU", "BB", "PG", "BS", "PK", "PY", "BH", "PA", "BR", "BY", "BY", "BM", "BG", "BJ", "BE",
                        "IS", "PR", "PL", "BA", "BO", "BZ", "BW", "BT", "VI", "VG", "BF", "BI", "BV", "KP", "GQ", "DK",
                        "DE", "TP", "TG", "DO", "DM", "RU", "EC", "FR", "PF", "GF", "TF", "VA", "PH", "FJ", "FI", "CV",
                        "FK", "GM", "CG", "CO", "CR", "GD", "GL", "GE", "CU", "GP", "GU", "GY", "KZ", "HT", "KR", "NL",
                        "HN", "KI", "DJ", "KG", "GN", "GW", "CA", "GH", "GA", "KH", "CZ", "ZW", "CM", "QA", "KY", "KM",
                        "KW", "CC", "HR", "KE", "CK", "LV", "LS", "LA", "LBLT", "LR", "LY", "LI", "LU", "RW", "RO",
                        "MG", "MV", "MT", "MW", "MY", "ML", "MH", "MU", "MR", "US", "UM", "MN", "BD", "PE", "FM", "MM",
                        "MD", "MA", "MC", "MZ", "MX", "NA", "ZA", "AQ", "YU", "NR", "NP", "NI", "NE", "NG", "NU", "NO",
                        "PW", "PN", "PT", "JP", "SE", "CH", "SV", "SL", "SN", "CY", "SC", "SA", "CX", "ST", "SH", "LC",
                        "SM", "LK", "SK", "SI", "SZ", "SD", "SR", "SU", "SB", "SO", "TJ", "TH", "TZ", "TO", "TT", "TN",
                        "TV", "TR", "TM", "TK", "GT", "VE", "BN", "UG", "UA", "UY", "UZ", "ES", "EH", "WS", "GR", "CI",
                        "SG", "NC", "NZ", "HU", "SY", "JM", "AM", "YE", "IQ", "IR", "IL", "IT", "IN", "ID", "GB", "UK",
                        "IO", "JO", "VN", "ZM", "ZR", "TD", "GI", "CL", "CF", "CN", "MO", "TW", "HK"]
        data: List = []
        for country in country_list:
            country_query = "{query} && country=\"{country}\"".format(query=query, country=country)
            # print(country_query)
            query_data = self.query(query=country_query, size=9999)
            data = data + query_data

        set_data: List = []
        for url in data:
            if url not in set_data:
                set_data.append(url)
        return set_data

    def get_subdomain(self, query: str) -> List:
        """
        获取domain 输出子域名
        :param query: domain:str
        :return: [domain:ip:port]
        """
        if self.error == True:
            return []

        # 子域名请求补全
        domain_query = "domain = {query}".format(query=query)
        domain_data = self.query(query=domain_query)
        return domain_data
        pass
