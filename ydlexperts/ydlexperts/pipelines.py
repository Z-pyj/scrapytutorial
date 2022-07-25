# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
from itemadapter import ItemAdapter



# 处理后的item存入MongoDB
class MongoDBPipeline(object):
    def __init__(self, connection_string, database):
        self.connection_string = connection_string
        self.database = database

    # 类方法，已依赖注入的方式实现的，方法参数就是crawler，通过crawler可以拿到全局配置的每个配置信息
    # 拿到配置信息后返回类对象即可，主要用来获取settings.py中的配置
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            connection_string=crawler.settings.get('MONGODB_CONNECTION_STRING'),
            database=crawler.settings.get('MONGODB_DATABASE')
        )

    # 当spider被开启时，被调用，主要进行一些初始化操作
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.connection_string)
        self.db = self.client[self.database]

    # 执行数据插入操作，直接调用insert_one方法传入item对象即可将数据存储到MongoDB中
    def process_item(self, item, spider):
        name = item.__class__.__name__
        self.db[name].insert_one(dict(item))
        return item

    # 当spider被关闭时被调用，将数据库链接关闭
    def close_spider(self, spider):
        self.client.close()

