# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LazadaCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    link = scrapy.Field()
    org_price = scrapy.Field()
    new_price = scrapy.Field()
    desc = scrapy.Field()
    brand = scrapy.Field()
    discount = scrapy.Field()
    rating = scrapy.Field()
    categories = scrapy.Field()
    spec = scrapy.Field()
    pass
