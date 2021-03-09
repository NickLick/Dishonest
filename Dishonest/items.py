# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy

class DishonestItem(scrapy.Item):
    # define the fields for your item here like:
    # 失信人名称
    name = scrapy.Field()
    # 失信人证件号码
    card_num = scrapy.Field()
    # 失信人年龄,企业都是0
    age = scrapy.Field()
    # 区域
    area = scrapy.Field()
    # 法人
    business_entity = scrapy.Field()
    # 失信内容
    content = scrapy.Field()
    # 公布日期
    publish_date = scrapy.Field()
    # 执行单位
    publish_unit = scrapy.Field()
    # 创建时间
    create_date = scrapy.Field()
    # 更新时间
    update_date = scrapy.Field()
