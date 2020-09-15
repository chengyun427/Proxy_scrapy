# -*- coding: utf-8 -*-
# 作者：Dr.叶子
# 创作日期：2020年9月12日
# github地址：https://github.com/chengyun427/Proxy_pool

# kuaidaili.py文件解释：
# 这是一个爬虫文件，具体生成步骤如下：
# 1.创建项目：scrapy startproject proxy
# 2.创建爬虫：scrapy genspider kuaidaili www.kuaidaili.com
# 3.运行指定爬虫名称：scrapy crawl kuaidaili

import scrapy
from proxy.items import KuaidailiItem


class KuaidailiSpider(scrapy.Spider):
    name = 'kuaidaili'      # 本爬虫名称
    allowed_domains = ['www.kuaidaili.com']     # 域名
    start_urls = ['https://www.kuaidaili.com/free/inha/1']     # 爬虫初始页，首先爬的是这一页

    p = 1   # 页码计数器
    pages = 2   # 请求总页数

    def parse(self, response):
        """
        接收请求start_urls链接成功后的response结果，筛选后传递到管道文件
        :param response: 请求返回的结果
        """
        # 1. 首先爬去第一页，也就是start_urls地址
        list_tr = response.selector.xpath("//div[@id='list']/table/tbody/tr")

        # 1.1 循环取数据
        for list_td in list_tr:
            # 1.1.1 创建Item
            item = KuaidailiItem()
            # 1.1.2 筛选数据
            item['ip'] = list_td.xpath("./td[@data-title='IP']/text()").extract_first()
            item['port'] = list_td.xpath("./td[@data-title='PORT']/text()").extract_first()
            item['degree'] = list_td.xpath("./td[@data-title='匿名度']/text()").extract_first()
            item['proxy_type'] = list_td.xpath("./td[@data-title='类型']/text()").extract_first()
            # 1.1.3 由于'位置position'与'运营商operator'字段是一个单元格的，所以这里做了下拆分
            position_operator = list_td.xpath("./td[@data-title='位置']/text()").extract_first()
            item['position'] = position_operator.rsplit(' ', 1)[0]
            item['operator'] = position_operator.rsplit(' ')[-1]
            # 1.1.4 处理“秒”字
            speed = list_td.xpath("./td[@data-title='响应速度']/text()").extract_first()
            item['speed'] = speed.rsplit('秒', 1)[0]
            item['last_time'] = list_td.xpath("./td[@data-title='最后验证时间']/text()").extract_first()
            # 1.1.4 传递到管道
            yield item

        # 2.循环改变路径，发起请求
        self.p += 1
        if self.p <= self.pages:
            next_url = 'https://www.kuaidaili.com/free/inha/' + str(self.p)
            url = response.urljoin(next_url)  # 构建绝对url地址
            yield scrapy.Request(url=url, callback=self.parse)  # 交给调度去继续爬取下一页信息
