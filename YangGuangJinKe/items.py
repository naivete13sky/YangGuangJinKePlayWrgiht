# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YangGuangJinKeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
    name = scrapy.Field()
    bdh = scrapy.Field()
    sfzh = scrapy.Field()
    self_mobile = scrapy.Field()

    pe_name = scrapy.Field()
    pe_mobile = scrapy.Field()

    jr_name = scrapy.Field()
    jr_mobile = scrapy.Field()

    ts_name = scrapy.Field()
    ts_mobile = scrapy.Field()

