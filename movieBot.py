#encoding:utf-8

'''
TODO : 智能搜索

THE WECHAT FUNCTION IN UNDER CONSTRUCTION, USE IT CAREFULLY !

power by Wyatt
2019/3/15

The WeChat Movie Bot, automatically send the movie resource BaiDu Cloud resource link,
the search engine is based on fqsousou.com, and the wechat engine is itchat

Enjoy It !

'''

#########   初始化开始     #########
mode_init = 1 #微信机器人初始状态，1表示开启，0则相反
bot_name = 'Wyatt电影机器人beta'
adv = 'Power By Wyatt\nAccuracy search based on Baidu Validate' #若不想加广告，赋 adv=''
get_movie_number = 5  #获取资源数量
validate_resource_max = 10 #验证资源链接的最大数量，若不想使用此功能，赋值为0
get_hot_number =5 #获取热门电影的个数，如果为0，则不获取
use_secrete_ip = 0 #是否用隐藏ip
error_dic = ['百度网盘-链接不存在','关注公众号获取资源','获取资源加'] #百度网盘关键词黑名单
send_online_watch_address = 5 # 发送在线观看链接的个数，0为不发送
baidu_short_link_token = '' # https://dwz.cn/console/userinfo 申请百度短网址的token
#########   初始化结束     #########


import requests as rq
import random
from lxml import etree
import itchat
import os
from lxml.html import fromstring
import json


# constant
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'}

if use_secrete_ip:
    try:
        ipLib = []
        url = 'https://www.xicidaili.com/nn/'
        r = etree.HTML(rq.get(url, headers=header).content)
        # //*[@id="ip_list"]/tr[2]/td[2]
        # //*[@id="ip_list"]/tr[3]/td[2]
        # //*[@id="ip_list"]/tr[101]/td[2]
        for i in range(2, 101):
            ip = r.xpath('//*[@id="ip_list"]/tr[' + str(i) + ']/td[2]/text()')[0]
            type = r.xpath('//*[@id="ip_list"]/tr[' + str(i) + ']/td[6]/text()')[0]
            port = r.xpath('//*[@id="ip_list"]/tr[' + str(i) + ']/td[3]/text()')[0]
            ipLib.append([ip,type,port])
    except Exception as e:
        print('匿名ip获取失败！：' + str(e))
        os._exit(0)

else:
    ipLib = []


def get_an_ip():
    global ipLib

    if ipLib == []:
        return {}
    choice = random.choice(ipLib)
    return {choice[1]:choice[0] + ':' + choice[2]}


def short(original_link):
    host = 'https://dwz.cn'
    path = '/admin/v2/create'
    url = host + path
    method = 'POST'
    content_type = 'application/json'
    token = '9860706e562a94413cc57f7076da665f'
    bodys = {'url': original_link}

    # 配置headers
    headers = {'Content-Type': content_type, 'Token': token}

    # 发起请求

    response = rq.post(url=url, data=json.dumps(bodys), headers=headers, proxies=get_an_ip())

    if json.loads(response.text)['Code'] == 0:
        return json.loads(response.text)['ShortUrl']
    else:
        return original_link

def validate_resource(test_url):

    global header,\
        error_dic

    r = rq.get(test_url,headers=header, proxies=get_an_ip()).content

    tree = fromstring(r)

    title = tree.findtext('.//title')

    for forbidden_parameter in error_dic:
        if forbidden_parameter in title:
            return 0
    return 1

def get_online_resource(movie_name):

    resource = []
    global header
    global send_online_watch_address

    r = rq.get('http://ifkdy.com/?q='+ movie_name,headers=header,proxies=get_an_ip()).content.decode()
    tree = etree.HTML(r)

    for i in range(1,send_online_watch_address):
        try:
            r = short(tree.xpath('/html/body/div[2]/div[1]/ul/li['+ str(i) +']/a/@href')[0])
        except IndexError:
            break

        resource.append(r)

    return resource

def gain_link(movie_name):

    global \
        header,\
        get_movie_number,\
        validate_resource_max

    c = rq.get('https://www.fqsousou.com/s/' + movie_name + '.html',headers=header, proxies=get_an_ip()).content.decode()
    tree_r = etree.HTML(c)

    r = []
    init = 1
    count = 0
    incorrect = []

    while True:
        try:
            rr = {}
            xpath = '/html/body/div[3]/div/div/div[2]/div[1]/div[2]/ul/li[' + str(init) + ']/a'
            treer = tree_r.xpath(xpath)
            rr['name'] = treer[0].attrib.get('title')
            rr['naive_link'] = treer[0].attrib.get('href')
            r.append(rr)
            init += 1

        # 这里不用打印error
        except Exception:
            break

    # 分析二级域名
    def ana_naive_link(naive_link):

        c = rq.get(naive_link,headers=header, proxies=get_an_ip()).content
        xpath_link = '/html/body/div[3]/div/div/div/div[1]/div[1]/div[3]/p/a[2]'
        xpath_type = '/html/body/div[3]/div/div/div/div[1]/div[1]/div[2]/dl/dt[2]/label/text()'
        xpath_size = '/html/body/div[3]/div/div/div/div[1]/div[1]/div[2]/dl/dt[3]/label/text()'
        c = etree.HTML(c)

        try:
            movie_link = short(c.xpath(xpath_link)[0].attrib.get('href'))
        except BaseException:
            movie_link = c.xpath(xpath_link)[0].attrib.get('href')

        movie_type = c.xpath(xpath_type)[0]

        if not movie_type == '文件夹':
            movie_size = c.xpath(xpath_size)[0]
        else:
            movie_size = ''

        return [movie_link, movie_type, movie_size]

    # 分析 movie number limit
    if len(r) < get_movie_number:
        gain_num_limit = len(r)
    else:
        gain_num_limit = get_movie_number

    # 遍历naive数组进一步分析资源地址
    for i in range(len(r)):
        try:

            resource = ana_naive_link('https://www.fqsousou.com/' + r[i]['naive_link'])

            # 有test_validate
            if validate_resource_max:
                if not validate_resource(resource[0]):
                    print('ok -- but validate error')
                    incorrect.append(i)
                    if i >= validate_resource_max:
                        break
                    continue

            # 如果没有test_validate 或 validate 正常
            # 注意pop后需要挪位
            r[i]['link'] = resource[0]

            if resource[1] == '':
                r[i]['type'] = '未知'
            else:
                r[i]['type'] = resource[1]

            if resource[2] == '':
                r[i]['size'] = '未知'
            else:
                r[i]['size'] = resource[2]


            print('ok')
            count += 1
            if count >= gain_num_limit:
                break


        except Exception as e:
            print('fail: ' + str(e))
            incorrect.append(i)
            continue

    # 倒序排列，以免出现pop错 index 的情况
    for i in sorted(incorrect,reverse=True):
        r.pop(i)

    # 最好参数不要带 gain_num_limit，以应对全 fail 的情况出现
    return r[:count]

# 微信机器人功能
def start_wechat_bot():

    global bot_name

    #如果是在服务器运行，auto_login 加上参数 enableCmdQR=2

    itchat.auto_login(hotReload=True)

    # initialize
    rcv = 'filehelper'
    itchat.send('成功接入'+ bot_name +'服务端！\n发送开启以开启服务',rcv)

    friend = itchat.get_friends()
    myName = friend[0]['UserName']

    def send_error_report(desc,error):
        itchat.send(desc+ '\n错误类型：'+ str(error),rcv)

    # 配置装饰器
    @itchat.msg_register(itchat.content.TEXT)
    def main(msg):

        # 导入初始化值
        global mode_init,\
            get_hot_number,\
            adv,\
            send_online_watch_address

        # return para: FromUserName ToUserName Content

        if msg['ToUserName'] == rcv:

            # 配置功能
            if msg['Content'] == '开启':
                mode_init = 1
                itchat.send('已开启机器人',rcv)
            if msg['Content'] == '状态':
                if mode_init:
                    itchat.send('已开启机器人\n发送关闭以关闭机器人',rcv)
                else:
                    itchat.send('未开启机器人',rcv)
            if msg['Content'] == '关闭':
                mode_init = 0
                itchat.send('已关闭机器人\n发送开启以启动机器人', rcv)
            if msg['Content'] == '测试':

                try:
                    beautiful_input(gain_link('我'))
                    itchat.send('搜索模块正常！',rcv)
                except Exception as e:
                    send_error_report('搜索模块错误！',e)
                try:
                    beautiful_input_for_hot_movie(get_hot())
                    itchat.send('热门模块正常！',rcv)
                except Exception as e:
                    send_error_report('热门模块错误！',e)

        # 对外功能
        if mode_init:
            if msg['Content'][:2] == '搜索':

                # 防止自己不能搜索
                if msg['FromUserName'] == myName:
                    msg['FromUserName'] = rcv

                itchat.send(bot_name + '正在搜索，请稍等。。。', msg['FromUserName'])
                try:
                    r = gain_link(msg['Content'][2:])
                    if not r == []:
                        re = beautiful_input(r)
                        itchat.send(re, msg['FromUserName'])
                    else:

                        # 如果没有检索
                        itchat.send('已检索到10个相关资源，但是 Baidu Validate 系统排除有 10 个垃圾资源')

                # 如果检索错误
                except Exception as e:
                    itchat.send('对不起，不能找到您想搜索的资源', msg['FromUserName'])
                    send_error_report('搜索模块错误，未能成功完成检索',e)

                # 获取在线看地址
                try:
                    if send_online_watch_address:
                        r = get_online_resource(msg['Content'][2:])
                        if not r == []:

                            re = '在线看地址：\n'
                            for i in r:
                                re = re + short(i) + '\n=====================\n'

                            itchat.send(re, msg['FromUserName'])

                # 如果错误
                except Exception as e:
                    send_error_report('在线看模块错误，未能成功完成检索', e)

                # 热门获取模块
                try:
                    if get_hot_number:
                        itchat.send(beautiful_input_for_hot_movie(r=get_hot()),msg['FromUserName'])
                except Exception as e:
                    send_error_report('热门模块错误，未能成功完成检索',e)

                # 如果 adv 不为空
                if not adv == '':
                    try:
                        itchat.send(str(adv),msg['FromUserName'])
                    except Exception as e:
                        send_error_report('广告模块错误',e)

    # 开始运行
    itchat.run()

# 热门功能
def get_hot():
    hot_list = []

    global \
        header,\
        get_hot_number

    # 不要加 proxies，不然会很慢
    c = rq.get('http://58921.com/boxoffice/live',headers=header,proxies=get_an_ip()).content.decode()
    r = etree.HTML(c)

    for i in range(1,get_hot_number + 1):
        xpath =  '//*[@id="content"]/div/table/tbody/tr['+ str(i+1) +']/td[1]/a/text()'
        try:
            hot_list.append(r.xpath(xpath)[0])
        except Exception as e:
            print(e)
            continue
    return hot_list

def beautiful_input(r):
    re = '百度云链接：\n=====================\n'
    for i in r:
        re = re + '资源名：' + i['name'] + '\n' + '资源类型：' + i['type'] + '\n' \
                  '资源大小：' + i['size'] + '\n云盘地址：' + i[
                  'link'] + '\n=====================\n'
    return re

def beautiful_input_for_hot_movie(r):
    re = ''
    count = 1
    for i in r:
        re = re + str(count) + '. ' + i + '\n'
        count += 1
    return '为您推荐目前最热的电影：\n' + re

def state_config():
    '''
    mode_init = 0
    get_movie_number = 5
    validate_resource_max = 0
    get_hot_number = 5
    use_secrete_ip = 0
    '''
    state = ''
    if mode_init == 0:
        print('微信机器人初始化状态为：关闭')
    else:
        print('微信机器人初始化状态为：开启')
    print('获取电影资源的数目为：' + str(get_movie_number))
    if validate_resource_max:
        print('最大百度云资源验证数目为：'+ str(validate_resource_max))
    if validate_resource_max == 0:
        print('未启用资源验证系统')
    if get_hot_number:
        print('获取最热电影数目：' + str(get_hot_number))
    if not get_hot_number:
        print('未启用最热电影系统')
    if use_secrete_ip:
        print('使用ip为：隐秘ip' )
    else:
        print('未开启隐秘IP')

    if adv == '':
        print('未开启广告投放功能')
    else:
        print('广告: ' + adv)

def help():
    print(
          '欢迎使用 MovieBot 姬，以下是你可以调用的函数：\n'
          'get_an_ip() -------------------- 从IP库里面随机获取一个高匿IP\n'
          'short(url)  -------------------- 缩短网址\n'
          'validate_resource(url) --------- 检测百度云资源可不可用\n'
          'get_online_resource(movie) ------- 获取在线看资源\n'
          'gain_link(movie) --------------- 获取资源\n'
          'start_wechat_bot() ------------- 开启微信服务\n'
          'get_hot() ---------------------- 获取热门电影\n'
          'beautiful_input(get_link) ------ 美化 get_link 的输出\n'
          'beautiful_input_for_hot_movie()- 美化 get_hot 输出\n'
          'state_config() ----------------- 打印易懂的 config\n'
          'help() ------------------------- 打印帮助\n'
          '\nWARNING: 在使用上述函数前，请先对初始化块进行赋值'
    )

