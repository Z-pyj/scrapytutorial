# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YdlexpertsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    expertName = scrapy.Field()
    footnotelabel = scrapy.Field()
    numberOfSpaces = scrapy.Field()
