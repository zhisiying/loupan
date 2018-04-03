# -*- coding: utf-8 -*-


# class LoupanPipeline(object):
#     def process_item(self, item, spider):
#         return item
import pymongo

class MongolPipeline(object):
    def __init__(self,mongo_url,mongo_db):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db
    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_url=crawler.settings.get('MONGO_URL'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )
    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]
    def process_item(self,item,spider):
        name = item.__class__.__name__
        self.db[name].insert(dict(item))
        print(item)
        print(self.db[name].find_one())
    def close_spider(self,spider):
        self.client.close()
