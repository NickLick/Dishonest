# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
import random
from Dishonest.settings import USER_AGENTS
import requests
from Dishonest.spiders.gsxt import GsxtSpider
from Dishonest.settings import COOKIE_LIST, COOKIES_KEY, COOKIES_PROXY_KEY, COOKIES_USER_AGENT_KEY
from scrapy.downloadermiddlewares.redirect import RedirectMiddleware


class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        # 设置随机user-agent
        # 如果是公示系统爬虫，直接跳过
        if isinstance(spider, GsxtSpider):
            return None
        else:
            request.headers['User-Agent'] = random.choice(USER_AGENTS)
            return None


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        # 设置代理ip
        # 如果是公示系统爬虫，直接跳过
        if isinstance(spider, GsxtSpider):
            return None
        else:
            # 1.获取代理协议
            protocol = request.url.split('://')[0]
            # 2.构建请求代理ip池的球球url
            proxy_url = 'http://127.0.0.1:8888/random?protocol={}'.format(protocol)
            # 3.发送请求
            response = requests.get(proxy_url)
            # 4.获取代理ip设置
            request.meta['proxy'] = response.content.decode()
            return None


class GsxtCookieMiddleware(object):
    # 公示系统中间件类
    def process_request(self, request, spider):
        if isinstance(spider, GsxtSpider):
            # 从cookie列表中随机获取一个cookie字典
            cookies_dict = random(COOKIE_LIST)
            print(cookies_dict)
            # 把cookie信息设置给request
            request.headers['User-Agent'] = cookies_dict[COOKIES_USER_AGENT_KEY]
            request.meta['Proxy'] = cookies_dict[COOKIES_PROXY_KEY]
            request.cookies = cookies_dict[COOKIES_KEY]
            # 设置不要重定向
            request.meta['dont_redirect'] = True
        else:
            return None

    def process_response(self, request, response, spider):
        if response.status != 200 or response.body == b'':
            # 备份请求
            req = request.copy()
            # 设置不过滤
            req.dont_filter = True
            # 交给引擎
            return req
        return response
