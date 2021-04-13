import scrapy
import json
from datetime import datetime
from jsonpath import jsonpath
from Dishonest.items import DishonestItem


# 设置起始url
# 生成所有页面的请求
# 解析页面，提取需要的数据

class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['baidu.com']
    start_urls = ['https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query=失信人&pn=0&rn=10&oe=utf-8']

    def parse(self, response):
        # 解析第一个请求
        # 来构建所有的url
        results = json.loads(response.text)
        # 取出总数据条数
        disp_num = jsonpath(results, '$..dispNum')[0]
        print(disp_num)
        # url模板
        url_pattern = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query=失信人&pn={}&rn=10&oe=utf-8'
        # 每隔10条数据，构建一个请求
        for pn in range(0, disp_num, 10):
            # 构建url
            url = url_pattern.format(pn)
            # 创建请求，交给引擎
            yield scrapy.Request(url, callback=self.parse_data)

    def parse_data(self, response):
        # 解析后续请求返回的数据
        datas = json.loads(response.text)
        disp_datas = jsonpath(datas, '$..disp_data')
        print(disp_datas)
        print(len(disp_datas))
        # 遍历结果列表
        for disp_data in disp_datas:
            item = DishonestItem()
            item['name'] = disp_data['iname']
            item['card_num'] = disp_data['cardNum']
            item['age'] = int(disp_data['age'])
            item['area'] = disp_data['areaName']
            item['business_entity'] = disp_data['businessEntity']
            item['content'] = disp_data['duty']
            item['publish_date'] = disp_data['publishDate']
            item['publish_unit'] = disp_data['courtName']
            item['create_date'] = datetime.now().strftime('%Y-%m-%d $H:%M:%S')
            item['update_date'] = datetime.now().strftime('%Y-%m-%d $H:%M:%S')
            # 把数据交给引擎
            print(item)
            yield item
