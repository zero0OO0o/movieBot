# Movie Bot

> 微信电影资源机器人



## 还在 debug 中，请先不要上机！！




## 功能

1. 实现电影资源抓取（抓取源：fqsousou）
2. 自动缩短资源链接
3. 实现微信对接

## 示意图

**朋友：** 搜索驯龙高手3



**机器人：** 正在搜索，请稍后。。。

​		搜索到以下资源：

​		++++++++++++++++++

​		海王【1080p】

​		网址：t.cn/asjasdjik

​		++++++++++++++++++

​		海王TV版

​		网址：t.cn/asdxd

​		++++++++++++++++++

## 点码调用示例
```python
# 搜索电影资源,返回5个结果，返回值为dict
print(gain_link(movie_name='猛龙过江',catch_number=5))
# 美化输出
print(beautiful_input(r=gain_link(movie_name='猛龙过江',catch_number=10)))
# 搜索5个热门电影，返回list
print(get_hot(5))
# 接入微信机器人
main()
# 缩短链接
print(short('pornhub.com/i/aksdnxaisiasnx'))
```