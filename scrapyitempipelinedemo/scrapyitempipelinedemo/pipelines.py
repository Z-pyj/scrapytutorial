# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
from scrapyitempipelinedemo.items import MovieItem
from elasticsearch import Elasticsearch
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class MongoDBPipeline(object):

    # 类方法，已依赖注入的方式实现的，方法参数就是crawler，通过crawler可以拿到全局配置的每个配置信息
    # 拿到配置信息后返回类对象即可，主要用来获取settings.py中的配置
    @classmethod
    def from_crawler(cls, crawler):
        cls.connection_string = crawler.settings.get('MONGODB_CONNECTION_STRING')
        cls.database = crawler.settings.get('MONGODB_DATABASE')
        cls.collection = crawler.settings.get('MONGODB_COLLECTION')
        return cls()

    # 当spider被开启时，被调用，主要进行一些初始化操作
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.connection_string)
        self.db = self.client[self.database]

    # 执行数据插入操作，直接调用insert_one方法传入item对象即可将数据存储到MongoDB中
    def process_item(self, item, spider):
        self.db[self.collection].update_one({
            'name': item['name']
        }, {
            '$set': dict(item)
        }, True)
        return item

    # 当spider被关闭时被调用，将数据库链接关闭
    def close_spider(self, spider):
        self.client.close()


class ElasticsearchPipeline(object):

    # 类方法，已依赖注入的方式实现的，方法参数就是crawler，通过crawler可以拿到全局配置的每个配置信息
    # 拿到配置信息后返回类对象即可，主要用来获取settings.py中的配置
    @classmethod
    def from_crawler(cls, crawler):
        cls.connection_string = crawler.settings.get('ELASTICSEARCH_CONNECTION_STRING')
        cls.index = crawler.settings.get('ELASTICSEARCH_INDEX')
        return cls()

    # 当spider被开启时，被调用，主要进行一些初始化操作
    def open_spider(self, spider):
        self.conn = Elasticsearch([self.connection_string])
        if not self.conn.indices.exists(self.index):
            self.conn.indices.create(index=self.index)

    def process_item(self, item, spider):
        self.conn.index(index=self.index, body=dict(item), id=hash(item['name']))
        return item

    def close_spider(self, spider):
        self.conn.transport.close()


class ImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        movie = request.meta['movie']
        type = request.meta['type']
        name = request.meta['name']
        file_name = f'{movie}/{type}/{name}.jpg'
        return file_name

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Image Downloaded Failed')
        return item

    def get_media_requests(self, item, info):
        for director in item['directors']:
            director_name = director['name']
            director_image = director['image']
            yield Request(director_image, meta={
                'name': director_name,
                'type': 'director',
                'movie': item['name']
            })

        for actor in item['actors']:
            actor_name = actor['name']
            actor_image = actor['image']
            yield Request(actor_image, meta={
                'name': actor_name,
                'type': 'actor',
                'movie': item['name']
            })
