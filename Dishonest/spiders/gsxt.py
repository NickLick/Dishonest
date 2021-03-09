import scrapy
import json
from Dishonest.items import DishonestItem
import re
from datetime import datetime


class GsxtSpider(scrapy.Spider):
    # 解析页面中的城市名称和id，构建公告信息和url
    # 解析失信企业公告信息
    name = 'gsxt'
    allowed_domains = ['gsxt.gov.cn']
    start_urls = 'http://www.gsxt.gov.cn/corp-query-entprise-info-xxgg-100000.html'
    # 失信企业的公告信息 ,获取数据的url
    data_url = 'http://www.gsxt.gov.cn/affiche-query-area-info-paperall.html?noticeType=11&areaid=100000&noticeTitle=&regOrg={}'

    def parse(self, response):
        # print(response.status)
        # print(response.text)
        # 获取包含省的名称、div标签列表
        divs = response.xpath('//div[@class="lable-list"]/div')
        for div in divs:
            area = div.xpath('./lable/text()').extract_first()
            id = div.xpath('./@id').extract_first()
            # print("%s:%s" % (area, id))
            data_url = self.data_url.format(id)
            for i in range(0, 50, 10):
                data = {
                    'start': str(i),
                    'length': '10'
                }
                yield scrapy.FormRequest(data_url, formdata=data, callback=self.parse_data, meta={'area': area})

    def parse_data(self, response):
        # 取出传递的区域
        area = response.meta['area']
        # print(response.text)
        # json格式转换为字典
        results = json.loads(response.text)
        # 获取公告信息列表
        datas = results['data']
        # 获取每一个公告信息
        for data in datas:
            item = DishonestItem()
            # 获取通知标题
            notice_title = data['noticeTitle']
            # 获取通知内容
            notice_content = data['noticeContent']
            # 取出名字
            name = re.findall('关?于?(.+?)的?列入.*', notice_title)
            item['name'] = name[0] if len(name) != 0 else ''
            name_cardnum = re.findall('经?查?,?(.+)\s* (统一社会信用代码/注册号: (\w+)):.*', notice_content)
            if len(name_cardnum) != 0:
                item['name'] = name_cardnum[0][0]
                item['card_num'] = name_cardnum[0][1]
            # 都是企业,都是0
            item['age'] = 0
            item['area'] = area
            item['business_entity'] = ''
            item['content'] = notice_content
            item['publish_date'] = datetime.fromtimestamp(data['noticeDate'] / 1000).strftime('%Y-%m-%d')
            item['publish_unit'] = data['judAuth_CN']
            item['create_date'] = datetime.now().strftime('%Y-%m-%d $H:%M:%S')
            item['update_date'] = datetime.now().strftime('%Y-%m-%d $H:%M:%S')
            # 把数据交给引擎
            print(item)
            yield item
