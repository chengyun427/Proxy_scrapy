# -*- coding: utf-8 -*-
# 作者：Dr.叶子
# 创作日期：2020年9月12日

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

# items.py文件解释：
# 1.定义抓取的数据结构；
# 2.创建Item需要继承scrapy.Item类，并且定义类型为scrapy.Field的字段；

import scrapy


class ProxyItem(scrapy.Item):
    """
    创建项目时候自动生成（默认空Item）
    """
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class KuaidailiItem(scrapy.Item):
    """
    kuaidaili爬虫的Item（自定义）
    """
    ip = scrapy.Field()  # ip
    port = scrapy.Field()  # port
    degree = scrapy.Field()  # 匿名度
    proxy_type = scrapy.Field()  # 类型
    position = scrapy.Field()  # 位置
    operator = scrapy.Field()  # 运营商
    speed = scrapy.Field()  # 响应速度
    last_time = scrapy.Field()  # 最后验证时间
