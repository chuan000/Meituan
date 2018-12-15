# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
import pymongo
from Meituan.items import MeituanItem, MeituanInfosItem


class MeituanPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'), mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db[MeituanItem.collection].create_index([('poi_id', pymongo.ASCENDING)])
        self.db[MeituanInfosItem.collection].create_index([('poi_id', pymongo.ASCENDING)])

    def process_item(self, item, spider):
        if isinstance(item, MeituanItem) or isinstance(item, MeituanInfosItem):
            self.db[item.collection].update({'poi_id': item.get('poi_id')}, {'$set': item}, True)
        return item


class TimePipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, MeituanItem) or isinstance(item, MeituanInfosItem):
            now = time.strftime('%Y-%m-%d %H:%M', time.localtime())
            item['create_time'] = now
            item['update_time'] = now
        return item

