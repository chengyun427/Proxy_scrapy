# Python爬虫实战之：快代理搭建IP代理池（Scrapy进阶版）

**CSDN博客：** [Python爬虫实战之：快代理搭建IP代理池（Scrapy进阶版）](https://blog.csdn.net/LTAO427/article/details/108577539).


# 前言
> 你好，我是Dr.叶子，用心写最优美的博客，弹最好听的钢琴！


# 项目背景
> - 之前写了篇简版的作为入门，链接: [Python爬虫实战之：快代理搭建IP代理池（简版）](https://blog.csdn.net/LTAO427/article/details/108524627)。为了进一步提升自己的能力，整理了这篇Scrapy进阶版。
> - 网上的一些知识太过于零散，项目代码不规范，所以亲自搭建实战项目，与大家分享！


# 项目简介
> 本项目主要基于Scrapy框架搭建爬虫，爬取快代理网站的IP数据，经过有效性验证后，储存到PostgreSQL，形成IP代理池，方便以后开展更多的爬虫项目，能防止个人IP被封锁。


# 项目演示
**1. Json 文件：**

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200915015459974.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0xUQU80Mjc=,size_16,color_FFFFFF,t_70#pic_center)


**2. 数据库：**

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200915015030243.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0xUQU80Mjc=,size_16,color_FFFFFF,t_70#pic_center)


**3. 最终生成：** 多出2个文件，Log 和 Json 文件

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200915015651246.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0xUQU80Mjc=,size_16,color_FFFFFF,t_70#pic_center)


#  后语
> 1. 原创内容，转载说明出处哦！
> 2. 以上内容本人整理，亲测可行，如有任何问题，敬请指正，谢谢~~
> 3. 点赞、收藏、也欢迎打赏，我弹钢琴你听呀~~哈哈！
