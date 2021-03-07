import scrapy


class GsxtSpider(scrapy.Spider):
    name = 'gsxt'
    allowed_domains = ['gsxt.gov.cn']
    start_urls = 'http://www.gsxt.gov.cn/corp-query-entprise-info-xxgg-100000.html'

    def parse(self, response):
        pass
