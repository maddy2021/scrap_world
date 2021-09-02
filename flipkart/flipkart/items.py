# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FlipkartItem(scrapy.Item):
    # define the fields for your item here like:
    domain_name = scrapy.Field()
    product_link = scrapy.Field()
    product_name = scrapy.Field()
    product_price = scrapy.Field()
    product_original_price = scrapy.Field()
    bread_crumb = scrapy.Field()
    product_rating = scrapy.Field()
    product_features = scrapy.Field()
    # url_is_valid = scrapy.Field()
    status_code = scrapy.Field()
    seller_details = scrapy.Field()
    highlights = scrapy.Field()
    pass