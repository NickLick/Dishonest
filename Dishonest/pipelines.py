# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from Dishonest.settings import MONGO_URL

# 1.建立数据库连接，获取操作数据库的cursor
# 2.关闭数据库，关闭cursor
# 3.如果数据不存在，包存，否则，跳过


class DishonestPipeline(object):
    def open_spider(self, spider):
        # 连接mongodb
        self.client = MongoClient(MONGO_URL)
        # 指定操作的集合
        self.col = self.client['dishonest_person_pool']['dishonest_persons']

    def close_spider(self, spider):
        # 关闭数据库连接
        self.client.close()

    def process_item(self, item, spider):
        # 数据不存在，保存数据
        # 自然人根据身份证号判断
        # 企业、组织根据区域+名称判断
        # 根据年龄判断个人还是组织/企业
        if item['age'] == 0:
            cursor = self.col.find({}, {'area': item['area'], 'name': item['name']})
        else:
            # 为了保证数据一致性
            # 如果是自然人，就替换掉身份证号的月份以及日期
            card_num = item['card_num']
            card_num = card_num[:10] + '****' + card_num[14:]
            item['card_num'] = card_num
            cursor = self.col.find({'card_num': item['card_num']})
        lists = []
        for item in cursor:
            lists.append(item)
        count = len(lists)
        if count == 0:
            # 如果没有数据，就插入数据
            spider.logger.info('插入数据:{}'.format(item))
            self.col.insert_one(dict(item))

        else:
            spider.logger.info('{}已存在,取消插入'.format(item))

