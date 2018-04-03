# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from selenium import webdriver
from ..items import *

driver = webdriver.Chrome()
driver.implicitly_wait(5)


class LianjiasSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['lianjia.com', ]
    f = open('C:\\Users\Administrator\Desktop\loupan\loupan\spiders\keyword.txt')
    start_urls = ['https://%s.lianjia.com/loupan' % m for m in f.read().split()]

    def parse(self, response):
        driver.get(response.url)
        page = driver.find_elements_by_xpath('//div[@class="page-box"]/a')
        list = []
        for i in page:
            list.append(i.text)
        try:
            list.pop()
            num = max(list)
        except:
            num = 1
        if num != 1:
            for pages in range(1, int(num)):
                print(pages)
                new_url = response.url + '/pg%s/' % pages
                yield scrapy.Request(new_url, callback=self.remen_loupan)
        else:
            yield scrapy.Request(response.url, callback=self.remen_loupan)

    def remen_loupan(self, response):
        href = response.xpath('//ul[@class="resblock-list-wrapper"]/li/div/div[1]/a/@href').extract()
        for i in href:
            in_href = response.url.split('/loupan')[0] + i
            yield scrapy.Request(in_href, callback=self.in_href)

    def in_href(self, response):
        print(response.url)
        loader = ItemLoader(item=LoupanItem(), response=response)
        loader.add_xpath('title', '//h1/text()')
        loader.add_xpath('price', '//span[@class="junjia"]/text()')
        loader.add_xpath('lou_type', '//p[@class="wu-type "]/span[2]/text()')
        loader.add_xpath('location', '//div[@class="bottom-info"]//p[3]/span/@title')
        loader.add_xpath('open_time', '//p[@class="when"]/span[2]/text()')
        yield loader.load_item()
        print(loader.load_item())
