#encoding:utf-8

import requests as rq
from lxml import etree

url = 'http://movie.mtime.com/11348/plots.html'


# constant
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'}


def get_movie_info(url):

    content = ''
    count = 1

    r = rq.get(url,headers=header).content.decode()
    tree = etree.HTML(r)

    while True:
        try:

            xpath_first_letter = '//*[@id="paragraphRegion"]/div/div[2]/div[2]/p['+ str(count) +']/span/text()'
            xpath = '//*[@id="paragraphRegion"]/div/div[2]/div[2]/p['+ str(count) +']/text()'
            content = content + tree.xpath(xpath_first_letter)[0] +tree.xpath(xpath)[0] + '\n\n'
            count += 1
        except Exception:
            break

    return content

def get_movie_info_url(movie_name):

    global header

    url = 'http://search.mtime.com/search/?q=' + movie_name

    r = rq.get(url,headers=header).content

    print(r)

    tree = etree.HTML(r)

    return tree.xpath('//*[@id="moreRegion"]/li[1]/h3/a')

print(get_movie_info_url('猛龙过江'))