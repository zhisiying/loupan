# -*- coding: utf-8 -*-

from scrapy import Item, Field
from scrapy.loader.processors import *


class LoupanItem(Item):
    title = Field()
    price = Field()
    lou_type = Field()
    location = Field()
    open_time = Field()
    url = Field()
    