#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import etree
import urllib2
import matplotlib.pyplot as plt

city = '北京市'
startdate = '2015-01-01'
enddate = '2015-12-25'
# 设置支持中文显示
from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
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
    aqi_list = [int(x) for x in aqi_list] # 元素类型转为int
    return aqi_list
# 计算每周AQI平均值,返回一个平均值list
def get_weekData(aqi_list):
    start = 0
    week_avg = []
    for week_data in aqi_list:
        week_data = aqi_list[start:start+7]
        start = start + 7
        if week_data == []:
            break
        w_avg = sum(week_data) / 7
        week_avg.append(w_avg)
    return week_avg
# 绘折线图
def plot(data):
    # 设置style
    plt.style.use('bmh')
    # 设置图标标题
    str =  city.decode('utf-8') + startdate.decode('utf-8') + u'至' + enddate.decode('utf-8') + u'每周平均空气质量指数走势图'
    plt.title(str, fontproperties=font)
    # 设置x轴的文字
    plt.xlabel(u'日期', fontproperties=font)
    # 设置y轴文字
    plt.ylabel(u'空气质量指数', fontproperties=font)
    # 画每周平均数据图
    #配置一下坐标刻度等
    ax=plt.gca()
    # ax.set_xticks(np.linspace(0,20,num=10))
    # ax.set_xticklabels( (u'第一周', u'第二周', u'第三周', u'第四周', u'第五周',  u'第六周',  u'第七周',  u'第八周', u'第九周',u'第十周'), fontproperties=font)
    # ax.set_yticks(np.linspace(0,300,8))
    # ax.set_yticklabels( ('0', '50', '100', '150', '200','250','300','350'))
    #定义y
    y2 = get_weekData(data)
    # 定义x
    x2 = [x2 for x2 in range(len(y2))]

    plt.plot(x2, y2, color = 'blue', label=u'week average line')
    # add a legend
    plt.legend(loc='upper left', frameon=False)

    plt.plot(x2, y2, 'bo', color = 'red')
    plt.show()
# 绘制饼图
def pie(data):
    lv1, lv2, lv3, lv4, lv5, lv6 = 0, 0, 0, 0, 0, 0
    for aqi in data:
        if aqi in range(0, 51):
            lv1 = lv1 + 1
        elif aqi >= 50 and aqi <= 100:
            lv2 = lv2 + 1
        elif aqi >= 101 and aqi <= 150:
            lv3 = lv3 + 1
        elif aqi >=151 and aqi <= 200:
            lv4 = lv4 + 1
        elif aqi >= 201 and aqi <= 300:
            lv5 = lv5 + 1
        else:
            lv6 = lv6 + 1
    list =[lv1, lv2, lv3, lv4, lv5, lv6]
    labels = 'Good', 'Green', 'Moderate', 'Yellow', 'Lightly Polluted', 'Orange'
    colors = ['blue', 'green', 'gray', 'yellow', 'red', 'orange']
    explode = (0, 0.1, 0, 0, 0, 0)
    title = city.decode('utf-8') + startdate.decode('utf-8') + u'至' + enddate.decode('utf-8') + u' AQI分布图'
    plt.title(title, fontproperties=font)
    plt.pie(list, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=0)
    plt.show()
# 绘制柱状图
def histogram():
    pass

if __name__ == '__main__':
    data = getData()
    plot(data)
    pie(data)