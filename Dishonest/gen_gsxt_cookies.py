# 实现生成gdxt的cookie
from gevent import monkey

monkey.patch_all()
from gevent.pool import Pool

from Dishonest.settings import USER_AGENTS
import random
import requests
import re
import js2py
from Dishonest.settings import COOKIES_KEY, COOKIES_PROXY_KEY, COOKIES_USER_AGENT_KEY, COOKIE_LIST


class GenGsxtCookie(object):
    def __init__(self):
        # 创建协程池
        self.pool = Pool()

    def save_cookie_to_list(self):
        while True:
            try:
                # 实现一个方法，把一套的代理ip，user-agent，cookie绑定在一起的信息放到一个列表中
                # 随机获取一个user-agent
                user_agent = random.choice(USER_AGENTS)
                # 随机获取一个代理ip
                response = requests.get('http://127.0.0.1:8888/random?protocol=http')
                proxy = response.content.decode()
                # 把user - agent，通过请求头，设置给session对象
                session = requests.session()
                session.headers = {
                    'User-Agent': user_agent,
                }
                # 把代理ip，通过proxies，设置给session对象
                session.proxies = {
                    'http': proxy
                }
                # 使用session对象，发送请求，获取需要的cookie信息
                self.gen_cookie(session)

                # 把代理ip，user_agent，cookie放到字典中，存储到一个列表中
                cookies_dict = {
                    COOKIES_KEY: session.cookies,
                    COOKIES_PROXY_KEY: proxy,
                    COOKIES_USER_AGENT_KEY: user_agent
                }
                print(cookies_dict)
                COOKIE_LIST.append(cookies_dict)
                break
            except Exception as ex:
                print(ex)

    def gen_cookie(self, session):
        # 生成cookie
        first_url = 'http://www.gsxt.gov.cn/corp-query-entprise-info-xxgg-100000.html'
        # 获取request的session对象，可以自动合并cookie信息
        response = session.get(first_url)
        print(response.status_code)
        print(response.content.decode())
        # print(session.cookies)
        # print(response.headers)

        # 1.提取script标签中的js
        js = re.findall('<script>(.+?)</script>', response.content.decode())[0]
        js = js.replace('document.cookie=', '')
        js = js.replace('\'', '')
        js = js.replace('(', '')
        js = js.replace(')', '')
        js = js.replace('+', '')
        print(js)
        # 2.替换eval
        # js = js.replace('{eval(', '{code(')
        # print(js)
        # 3.执行js
        #  获取执行js环境
        # context = js2py.EvalJs()
        # context.execute(js)
        # print(context.code)
        # 获取生成cookie的js
        # cookie_code=re.findall("document.(cookie=.\+)\+';Expires",content.code)[0]
        # 观察发现，在js2py中，是不能使用‘document’，‘window’ 这些浏览器对象
        # js2py无法处理 自己看懂js
        # document赋值替换为网站根路径
        # cookie_code=re.sub()
        # context.execute(cookie_code)
        # print(context.cookie)

    def run(self):
        # 异步生成50个cookie字典,
        for i in range(50):
            self.pool.apply_async(self.save_cookie_to_list)
        # 主线程等待协程任务完后曾
        self.pool.join()


if __name__ == '__main__':
    ggc = GenGsxtCookie()
    ggc.run()
