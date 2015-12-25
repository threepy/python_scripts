#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import etree
import urllib2
import numpy as np
import matplotlib.pyplot as plt

city = '南京市'
startdate = '2015-01-01'
enddate = '2015-12-24'
# 获取数据
def getData():
    url = 'http://datacenter.mep.gov.cn/report/air_daily/air_dairy.jsp'
    page = 1
    get_url = url + '?city=' + city + '&startdate=' + startdate + '&enddate=' + enddate + '&page=' + str(page)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Host': 'datacenter.mep.gov.cn',
        'Referer': 	'http://datacenter.mep.gov.cn/report/air_daily/air_dairy.jsp',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
    }
    req = urllib2.Request(get_url, headers = headers)
    resp = urllib2.urlopen(req)
    content = resp.read()
    tree = etree.HTML(content)
    list = tree.xpath("//b/font[@color='#004e98']/text()")
    total_page = int(list[1])
    aqi_list = []
    # 获取时间区间的aqi数据
    for page in range(1, total_page+1):
        get_url = url + '?city=' + city + '&startdate=' + startdate + '&enddate=' + enddate + '&page=' + str(page)
        req = urllib2.Request(get_url, headers = headers)
        resp = urllib2.urlopen(req)
        content = resp.read()
        tree = etree.HTML(content)
        # 获取aqi值
        aqi_list2 = tree.xpath('//div/center/div/table/tr[position()>=3 and position()<last()-2]/td[4]/text()')
        aqi_list = aqi_list + aqi_list2
    aqi_list = aqi_list[::-1] # 倒序
    return aqi_list

# 绘图
def plot():
    from matplotlib.font_manager import FontProperties
    font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
    # 设置图标标题
    str =  city.decode('utf-8') + startdate.decode('utf-8') + u'至' + enddate.decode('utf-8') + u'空气质量指数走势图'
    plt.title(str, fontproperties=font)
    # 设置x轴的文字
    plt.xlabel(u'日期（天）', fontproperties=font)
    # 设置y轴文字
    plt.ylabel(u'空气质量指数', fontproperties=font)
    # 定义y轴
    y = getData()
    # 定义x轴
    x = [x for x in range(len(y))]

    plt.plot(x, y, color = 'blue', label='everyday')
    # add  a legend
    plt.legend(loc='upper left', frameon=False)
    plt.show()

if __name__ == '__main__':
    plot()