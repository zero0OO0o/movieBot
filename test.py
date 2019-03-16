#encoding:utf-8


import requests as rq
from lxml.html import fromstring

def test_resource_validate(test_url):

    error_dic = ['百度网盘-链接不存在','关注公众号获取资源']

    a1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)'}

    r = rq.get(test_url,headers=a1).content

    tree = fromstring(r)

    title = tree.findtext('.//title')

    for forbidden_parameter in error_dic:
        if forbidden_parameter in title:
            return 0
    return 1
