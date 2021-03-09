import scrapy
import json
from Dishonest.items import DishonestItem
from datetime import datetime


class CourtSpider(scrapy.Spider):
    name = 'court'
    allowed_domains = ['court.gov.cn']
    post_start_url = 'http://jszx.court.gov.cn/api/front/getPublishInfoPageList'

    # 重写起始请求方法
    def start_requests(self):
        data = {
            'pageSize': "10",
            'pageNo': "1",
        }
        # 构建post请求交给引擎
        yield scrapy.FormRequest(self.post_start_url, formdata=data, callback=self.parse)

    def parse(self, response):
        # 解析第一次请求数据获取总页数
        results = json.loads(response.text)
        page_count = results['pageCount']
        # 构建每一页的请求
        for page_no in range(page_count):
            data = {
                'pageSize': "10",
                'pageNo': str(page_no)
            }
            yield scrapy.FormRequest(self.post_start_url, formdata=data, callback=self.parse_data)

    def parse_data(self, response):
        # 解析数据
        results = json.loads(response.text)
        # 获取失信人信息列表
        datas = results['data']
        for data in datas:
            item = DishonestItem()
            item['name'] = data['name']
            item['card_num'] = data['cardNum']
            item['age'] = int(data['age'])
            item['area'] = data['areaName']
            item['business_entity'] = data['buesinessEntity']
            item['content'] = data['duty']
            item['publish_date'] = data['publishDate']
            item['publish_unit'] = data['courtName']
            item['create_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item['update_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 把数据交给引擎
            print(item)
            yield item
