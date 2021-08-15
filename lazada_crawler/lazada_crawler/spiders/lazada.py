import scrapy
import chompjs
import json
from .lazada_helper import scrap_product

# reference from: 
# https://github.com/yash0307jain/flipkart-web-scraper/blob/master/flipkart_scraper/spiders/flipkart_scraper.py
class LazadaSpider(scrapy.Spider):
    name = 'lazada'
    total_size = -1
    current_size = 0
    page_no = 1
    product_url_list = []
    # allowed_domains = ['lazada.sg']
    start_urls = ['https://www.lazada.sg/catalog/?_keyori=ss&from=input&page=1&q=tv&sort=popularity']
    PROTOCOL = "https:"

    def parse(self, response):
        # with open("oho.html","w+",encoding="utf-8") as fp:
        #     fp.write(response.text)
        # product_url_list = []
        javascript = response.css('script::text').get()
        data = chompjs.parse_js_object(javascript)
        if self.total_size==-1:
            self.total_size = int(data["mainInfo"]["totalResults"]) # 4080
        for product in data["mods"]["listItems"]:
            self.product_url_list.append(self.PROTOCOL + product["productUrl"])
        if(len(self.product_url_list)>0):
            yield scrapy.Request(url = self.product_url_list[0], callback = self.parse_item)
        # else:
        #     break
        self.current_size = self.current_size + 40  # because every page has 40 data
        self.page_no = self.page_no+1
        # print(self.product_url_list)
        # print(len(self.product_url_list))
        # if(self.current_size<=self.total_size):
        #     next_page_url= f'https://www.lazada.sg/catalog/?_keyori=ss&from=input&page={self.page_no}&q=tv&sort=popularity'
        #     yield scrapy.Request(url = next_page_url, callback = self.parse)

    def parse_item(self,response):
        # with open("product.html","w+",encoding="utf-8") as fp:
        #     fp.write(response.text)
        script_css = 'script:contains("__moduleData__")::text'
        script_pattern = r'__moduleData__ = (.*);'
        # warning: for some pages you need to pass replace_entities=True
        # into re_first to have JSON escaped properly
        script_text = response.css(script_css).re_first(script_pattern)
        # product_data=response.css('script:contains(__moduleData__)::text').re_first('__moduleData__=(.*)')
        json_data = chompjs.parse_js_object(script_text)
        # with open("product.json","w+") as fp:
        #     json.dump(json_data,fp)
        item_obj = scrap_product(json_data["data"]["root"])
        print(item_obj)
        yield item_obj

