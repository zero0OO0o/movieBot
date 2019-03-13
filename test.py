#encoding:utf-8

import requests as rq
import random
from lxml import etree
import itchat


def ana_naive_link(naive_link):
    c = rq.get(naive_link).content
    xpath_link = '/html/body/div[3]/div/div/div/div[1]/div[1]/div[3]/p/a[2]'
    xpath_type = '/html/body/div[3]/div/div/div/div[1]/div[1]/div[2]/dl/dt[2]/label/text()'
    xpath_size = '/html/body/div[3]/div/div/div/div[1]/div[1]/div[2]/dl/dt[3]/label/text()'
    c = etree.HTML(c)

    movie_link = c.xpath(xpath_link)[0].attrib.get('href')
    movie_type = c.xpath(xpath_type)
    movie_size = c.xpath(xpath_size)

    return [movie_link, movie_type, movie_size]


a = [1,2,[]]
print(a[2][0])
