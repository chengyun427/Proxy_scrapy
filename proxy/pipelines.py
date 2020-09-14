# -*- coding: utf-8 -*-
# 作者：Dr.叶子
# 创作日期：2020年9月12日

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# pipelines.py管道文件解释 ：
# 1.负责处理爬虫从网页中抽取的实体，主要的功能是持久化实体、验证实体的有效性、清除不需要的信息；
# 2.当页面被爬虫解析后，将被发送到项目管道，并经过几个特定的次序处理数据；
# 3.可以在setting.py自定义优先级，可以定义存为文件，也可以定义存数据库等多种class；

import json
import psycopg2
import requests
from faker import Factory
from scrapy import log


class ProxyPipeline(object):
    """
    默认空的管道类
    """

    def process_item(self, item, spider):
        return item


class KuaidailiJsonPipeline(object):
    """
    保存为json文件的管道类（自定义）
    """

    def __init__(self):
        self.f = open("kuaidaili_pipeline.json", "wb")

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False) + ", \n"
        self.f.write(content.encode("utf-8"))
        return item

    def close_spider(self, spider):
        self.f.close()


class KuaidailiPostgresPipeline(object):
    """
    保存到postgres数据库的管道类（自定义）
    """
    def __init__(self, host, user, password, database, port):
        """
        初始化函数
        :param host: 主机ip
        :param user: 数据库用户名
        :param password: 数据库密码
        :param database: 所属数据库
        :param port: 端口号
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.target_url = "https://www.baidu.com"  # 爬虫的目标地址，作为验证代理池ip的有效性
        # 步骤1：连接数据库
        self.db = psycopg2.connect(database=self.database, user=self.user,
                                   password=self.password, host=self.host, port=self.port)
        self.cur = self.db.cursor()

    @classmethod
    def from_crawler(cls, crawler):
        """
        搜寻器对象类（scrapy默认）
        提供对所有Scrapy核心的访问，诸如设置和信号之类的组件；
        :param crawler: 搜寻器
        :return: 返回给上面的初始化函数中__init__
        """
        return cls(
            host=crawler.settings.get("PGSQL_HOST"),
            user=crawler.settings.get("PGSQL_USER"),
            password=crawler.settings.get("PGSQL_PASS"),
            database=crawler.settings.get("PGSQL_DATABASE"),
            port=crawler.settings.get("PGSQL_PORT"),
        )

    def open_spider(self, spider):
        """
        当spider被开启时调用（scrapy默认）
        :param spider: spider对象
        """
        # 步骤2：清空数据库表
        self.clear_db()

    def process_item(self, item, spider):
        """
        当处理item数据时调用（scrapy默认必须）
        每个item pipeline组件都需要调用该方法，这个方法必须返回一个 Item
        或任何继承类对象，或是抛出 DropItem 异常，被丢弃的item将不会被之后的pipeline组件所处理。
        :param item: 被爬取的item
        :param spider: spider对象
        :return: item
        """

        ip_port = item["ip"] + ":" + item["port"]
        headers = {'User-Agent': Factory.create(locale='zh-CN').user_agent()}

        # 步骤3：验证ip是否有效
        if self.is_useful(ip_port, headers, self.target_url):

            data = (item["ip"], item["port"], item["degree"], item["proxy_type"],
                    item["position"], item["operator"], item["speed"], item["last_time"])
            sql = "insert into proxy.public.proxy(ip,port,degree,type,position,operator,speed,last_time) " \
                  "values(%s,%s,%s,%s,%s,%s,%s,%s)"

            try:
                # 步骤4：存入数据库
                self.cur.execute(sql, data)  # 执行sql
                self.db.commit()  # 事务提交
            except Exception as e:
                self.db.rollback()  # 发生错误时回滚
                log.msg("存入数据库失败：" + str(e), level=log.ERROR)

        # 返回给引擎，告诉引擎这里item已经处理结束
        return item

    def close_spider(self, spider):
        """
        当spider被关闭时调用（scrapy默认）
        关闭数据库连接
        :param spider: spider对象
        """
        # 步骤5：关闭数据库连接
        self.db.close()
        self.cur.close()

    def clear_db(self):
        sql = "TRUNCATE TABLE proxy.public.proxy RESTART IDENTITY"
        try:
            self.cur.execute(sql)   # 执行sql
            self.db.commit()  # 事务提交
        except Exception as e:
            self.db.rollback()  # 发生错误时回滚
            log.msg("清空proxy数据库失败：" + str(e), level=log.ERROR)

    @staticmethod
    def is_useful(ip_port, headers, target_url):
        """
        （自定义方法）
        判断ip是否可用。
        :param ip_port: ip+端口号
        :param headers: 随机请求头
        :param target_url: 爬虫的目标地址，作为验证代理池ip的有效性
        :return: bool
        """
        url = target_url    # 验证ip对目标地址的有效性
        proxy_ip = 'http://' + ip_port
        proxies = {'http': proxy_ip}
        flag = True
        try:
            requests.get(url=url, headers=headers, proxies=proxies, timeout=2)
            print("【可用】：" + ip_port)
        except Exception as e:
            log.msg("程序 is_useful 发生错误：" + str(e), level=log.ERROR)
            flag = False
        return flag
