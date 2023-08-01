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
    br_mobile = scrapy.Field()

    pe_name = scrapy.Field()
    pe_mobile = scrapy.Field()

    xd_name = scrapy.Field()
    xd_mobile = scrapy.Field()

    fq_name = scrapy.Field()
    fq_mobile = scrapy.Field()

    mq_name = scrapy.Field()
    mq_mobile = scrapy.Field()

    ts_name = scrapy.Field()
    ts_mobile = scrapy.Field()

    qt_name = scrapy.Field()
    qt_mobile = scrapy.Field()

    responseText = scrapy.Field()#网页内容
