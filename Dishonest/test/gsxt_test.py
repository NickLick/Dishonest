# 国家企业公示系统 url测试
import requests
import re
import js2py


def test_header_data():
    url = 'http://www.gsxt.gov.cn/affiche-query-area-info-paperall.html?noticeType=11&areaid=100000&noticeTitle=&regOrg' \
          '=110000 '
    # post 数据
    data = {
        #  'draw': '1',
        'start': '0',
        'length': '10'
    }
    headers_1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.82 Safari/537.36',
        'Cookie': '__jsluid_h=34522bb962c0afb8b0e92f84231e2ccf; '
                  '__jsl_clearance=1615038482.252|0|VMidapWem7KjIU%2BcMvc%2BmOmRQcM%3D'

    }
    response = requests.post(url, data=data, headers=headers_1)
    print(response.content.decode())


def test_cookie():
    first_url = 'http://www.gsxt.gov.cn/corp-query-entprise-info-xxgg-100000.html'
    headers_2 = {
        'User-Agent':  "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"
    }

    # 获取request的session对象，可以自动合并cookie信息
    session = requests.session()
    response = session.get(first_url, headers=headers_2)
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


if __name__ == '__main__':
    # test_header_data()
    test_cookie()
