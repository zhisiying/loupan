# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from gerapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.loader import ItemLoader
from ..items import *
from scrapy.loader.processors import *

class LianjiaSpider(CrawlSpider):
    name = 'lianjia'
    allowed_domains = ['lianjia.com',]
    custom_settings = {
        "ITEM_PIPELINES": {
            'gerapy.pipelines.MongoPipeline': 300,
        }
    }
    start_urls = ['https://bj.fang.lianjia.com/loupan/pg%s/' % i for i in range(1, 10)]
    rules = (
        Rule(
            LinkExtractor(restrict_xpaths=['//ul[@class="resblock-list-wrapper"]/li/div/div[1]/a'], ),
            callback='links_item', ),
    )

    def links_item(self, response):
        print(response.url)
        loader = ItemLoader(item=LoupanItem(), response=response)
        loader.add_xpath('title', '//h1/text()')
        loader.add_xpath('price', '//span[@class="junjia"]/text()')
        loader.add_xpath('lou_type', '//p[@class="wu-type "]/span[2]/text()')
        loader.add_xpath('location', '//div[@class="bottom-info"]//p[3]/span/@title')
        loader.add_xpath('open_time', '//p[@class="when"]/span[2]/text()')
        yield loader.load_item()
        print(loader.load_item())


