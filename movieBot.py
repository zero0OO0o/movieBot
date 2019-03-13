#encoding:utf-8

import requests as rq
import random
from lxml import etree
import itchat

def short_link(original_link):
    try:
        methodLib = ['c7','kks','u6','rrd']
        method = random.choice(methodLib)
        pc = {
            'url' : original_link,
            'type' : method
        }
        g = eval(rq.post('https://create.ft12.com/done.php?m=index&a=urlCreate',pc).content.decode())
        if g['status'] == 1:
            return g['list']
        else:
            return "解析失败！"
    except BaseException:
        return "解析异常！"

def short(link):
    return short_link(link)


def gain_link(movie_name,catch_number):
    c = rq.get('https://www.fqsousou.com/s/' + movie_name + '.html').content.decode()
    tree_r = etree.HTML(c)

    r = []
    init = 1
    count = 0

    while True:
        try:
            rr = {}
            xpath = '/html/body/div[3]/div/div/div[2]/div[1]/div[2]/ul/li[' + str(init) + ']/a'
            treer = tree_r.xpath(xpath)
            rr['name'] = treer[0].attrib.get('title')
            rr['naive_link'] = treer[0].attrib.get('href')
            r.append(rr)
            init += 1

        except BaseException:
            break

    def ana_naive_link(naive_link):
        c = rq.get(naive_link).content
        xpath_link = '/html/body/div[3]/div/div/div/div[1]/div[1]/div[3]/p/a[2]'
        xpath_type = '/html/body/div[3]/div/div/div/div[1]/div[1]/div[2]/dl/dt[2]/label/text()'
        xpath_size = '/html/body/div[3]/div/div/div/div[1]/div[1]/div[2]/dl/dt[3]/label/text()'
        c = etree.HTML(c)

        try:
            movie_link = short(c.xpath(xpath_link)[0].attrib.get('href'))
        except BaseException:
            movie_link = c.xpath(xpath_link)[0].attrib.get('href')

        movie_type = c.xpath(xpath_type)
        movie_size = c.xpath(xpath_size)

        return [movie_link, movie_type, movie_size]

    if len(r) < catch_number:
        gain_num_limit = len(r)
    else:
        gain_num_limit = catch_number

    for i in range(len(r) - 1):
        try:
            resource = ana_naive_link('https://www.fqsousou.com/' + r[i]['naive_link'])
            r[i]['link'] = resource[0]

            if resource[1] == []:
                r[i]['type'] = '未知'
            else:
                r[i]['type'] = resource[1][0]

            if resource[2] == []:
                r[i]['size'] = '未知'
            else:
                r[i]['size'] = resource[2][0]

            count += 1
            print('ok')
            if count == gain_num_limit:
                break
        except BaseException:
            print('fail')
            r.pop(i)
            continue
    return r[:gain_num_limit]

def main():
    itchat.auto_login(hotReload=True)

    # initialize
    rcv = 'filehelper'
    itchat.send('成功开启Wyatt电影助手服务端！',rcv)

    friend = itchat.get_friends()
    myName = friend[0]['UserName']

    # 初始化状态为：离线 (1表示在线)
    mode = 0


    # 配置装饰器
    @itchat.msg_register(itchat.content.TEXT)
    def main(msg):
        global mode

        # return para: FromUserName ToUserName Content

        if msg['ToUserName'] == rcv:
            if msg['Content'] == '开启':
                mode = 1

        if mode:
            if msg['FromUserName'] != myName and msg['Content'][:2] == '搜索':
                itchat.send('Wyatt电影机器人正在搜索，请稍等。。。', msg['FromUserName'])
                try:
                    r = gain_link(msg['Content'][2:])

                    re = '============================\n'
                    for i in r:
                        re = re + '资源名：' + i['name'] + '\n' + '资源类型：' + i['type'] + '\n' \
                                  '资源大小：' + i['size'] + '\n云盘地址：' + i[
                                  'link'] + '\n============================\n'

                    itchat.send(re, msg['FromUserName'])
                except BaseException:
                    itchat.send('对不起，不能找到您想搜索的资源', msg['FromUserName'])


    itchat.run()

def get_hot(movie_number):

    hot_list = []

    c = rq.get('https://www.fqsousou.com/').content.decode()
    r = etree.HTML(c)

    for i in range(1,movie_number + 1):
        xpath =  '/html/body/div[2]/div/div[3]/div/div[2]/ul[2]/li['+ str(i) +']/a/text()'
        try:
            hot_list.append(r.xpath(xpath)[0])
        except BaseException:
            continue
    return hot_list

def beautiful_input(r):
    re = '============================\n'
    for i in r:
        re = re + '资源名：' + i['name'] + '\n' + '资源类型：' + i['type'] + '\n' \
                  '资源大小：' + i['size'] + '\n云盘地址：' + i[
                  'link'] + '\n============================\n'
    return re


