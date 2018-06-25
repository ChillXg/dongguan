# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


#class DongguanPipeline(object):
    #def process_item(self, item, spider):
        #spider.item['name'] = item.sub('\xa0', ' ', spider.item['name'])

        #return item

'''
import codecs
import json

class JsonWriterPipeline(object):

    def __init__(self):
        # 创建一个只写文件，指定文本编码格式为utf-8
        self.filename = codecs.open('sunwz.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.filename.write(content)
        return item

    def spider_closed(self, spider):
        self.file.close()
'''

import pymongo
from scrapy.conf import settings

class SAVE_TO_MONGOPipeline(object):
    def __init__(self, mongo_uri, mongo_db):#初始化数据
        self.limit = 50
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
            )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item ,spider):
        name = item.__class__.__name__
        self.db[name].insert(dict(item))
        return item

    def close_spider(self,spider):
        self.client.close()
