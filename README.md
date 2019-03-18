# MovieBot 微信电影助手

![](logo.png)

*----- 简单的的微信电影姬接入程序 Simple WeChat MovieBot Solution*

## 基于

1. [番茄搜搜](https://fqsousou.com): 可能是中国资源最多、更新最快的pan资源站
2. ItChat: 基于python的非官方微信api库
3. [不知名的IP库站](https://www.xicidaili.com/nn/): 用来防止ip被ban
4. [百度缩短网址服务](https://dwz.cn):
5. [58921影视站](http://58921.com): 提供电影排名数据
6. [疯子搜索](http://ifkdy.com): 提供在线看地址

## 功能

1. 获取最新电影资源的百度云链接
2. 通过title黑名单来确保百度云的资源的可用性
3. 缩短网址
4. 实时更换ip，防止被ban
5. 获取最热门影视
6. 获取在线看地址
6. 微信傻瓜对接
7. 轻松配置广告

## 用法

懒得解释了，放个DEMO吧！

### 控制端

![](demo/4.jpg)



### 朋友端

![](demo/2.jpg)

![](demo/1.jpg)

## 使用

### 1. 配置`moviebot`

打开`moviebot.py`，并根据你的需求修改`初始化`栏目

```python
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
baidu_short_link_token = '*********************' # https://dwz.cn/console/userinfo 申请百度短网址的token
#########   初始化结束     #########
```

### 2. 运行`run.py`

运行后应该会出现一个二维码，打开你的微信扫一下并同意就可以了。如果接入成功的话你的`文件传输助手`应该会给你发如下的消息：

```txt
成功接入Wyatt电影机器人beta服务端！
发送开启以开启服务
```

### 3. 激活moviebot

收到消息后，只能表示你接入微信成功了，如果你想启用`moviebot`的话，微信给`文件传输助手`发送`开启`即可！

同时，当你不确定到底开没开启服务时，你可以发送消息`状态`查询

![](demo/5.png)

### 4. 最后

一旦你的朋友给你发送如下的消息的话：

```txt
搜索驯龙高手3 电影
```

他就可以收到关于`驯龙高手3 电影`电影资源的回复啦！

### 5. filehelper可调用的函数

**测试** : 检测函数是否可以运行
**开启** : 开启服务端
**关闭** : 关闭服务端
**状态** : 检测服务状态

## 开发者指南

### 1. 调用

> WARNING: 调用之前请先配置好`初始化`区域因为大多数方程的参数赋值方法用是`global`

**get_an_ip**() : 获取一个随机的可用的ip地址

**short()** : 缩短网址，e.g. short(‘baidu.com/asasdajncd11212’)

**validate_resource()** : 验证百度云资源是否有效，编辑`error_dic`以修改策略

**gain_link()** ： 搜索电影资源，e.g. gain_link(‘驯龙高手’)

**start_wechat_bot()** : 开启wechat服务端

**get_hot()** : 获取热门电影

**beautiful_input(gain_link())** : 美化`gain_link`的输出

**beautiful_input_for_hot_movie(get_hot())** : 美化`get_hot`的输出

**state_config()** : 打印初始化的配置

**get_online_resource()** : 获取在线看地址

**help()** : 获取可用函数帮助

## 更新

**V2**： 增加在线看功能，改变短网址API

**V1.1**：修复一些致命bug，简化代码，exe版诞生

**V1**：大体完成，能跑，似乎没bug

## 赞赏

如果觉得项目对你有用的话不妨请我喝杯冰阔落吧 (‾◡◝)

![](pay.jpg)

