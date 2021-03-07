# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
import random
from Dishonest.settings import USER_AGENT
import requests
from Dishonest.spiders.gsxt import GsxtSpider


class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        # 设置随机user-agent
        # 如果是公示系统爬虫，直接跳过
        if isinstance(spider, GsxtSpider):
            return None
        else:
            request.headers['User-Agent'] = random.choice(USER_AGENT)
            return None


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        # 设置代理ip
        # 如果是公示系统爬虫，直接跳过
        if isinstance(spider, GsxtSpider):
            return None
        else:
            # 1.获取代理协议
            protocol = request.url.spilit('://')[0]
            # 2.构建请求代理ip池的球球url
            proxy_url = 'http://127.0.0.1:16888/random?protocol={}'.format(protocol)
            # 3.发送请求
            response = requests.get(proxy_url)
            # 4.获取代理ip设置
            request.meta['proxy'] = response.content.decode()
            return None
