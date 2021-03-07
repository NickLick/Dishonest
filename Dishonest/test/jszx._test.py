# 法院信用公示 url 测试
import requests

url = 'http://jszx.court.gov.cn/api/front/getPublishInfoPageList'
# post 数据
data = {
    #  'pageCount': 0,
    #  'currentPage': 1,
    'pageSize': 10,
    'pageNo': 135916,
    # 'yearId': '0',
    # 'kqsId': '0',
    #  'keyword': '',
    # 'orderBy': 1,
    # 'pName': '公司',
    # 'pCardNum': ''
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/89.0.4389.82 Safari/537.36',
}

if __name__ == '__main__':
    response = requests.post(url, data=data, headers=headers)
    print(response.content.decode())
