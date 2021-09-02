import scrapy
import chompjs
import json
from bs4 import BeautifulSoup
from .lazada_helper import scrap_product
from ..items import LazadaCrawlerItem

# reference from: 
# https://github.com/yash0307jain/flipkart-web-scraper/blob/master/flipkart_scraper/spiders/flipkart_scraper.py
class LazadaSpider(scrapy.Spider):
    name = 'lazada'
    total_size = -1
    current_size = 0
    page_no = 1
    product_url_list = []
    # allowed_domains = ['lazada.sg']
    start_urls = ['https://www.lazada.sg/catalog/?_keyori=ss&from=input&page=1&q=baby+toys&sort=popularity']
    PROTOCOL = "https:"

    def parse(self, response):
        # with open("oho.html","w+",encoding="utf-8") as fp:
        #     fp.write(response.text)
        # product_url_list = []
        self.product_url_list = []
        try:
            javascript = response.css('script::text').get()
            data = chompjs.parse_js_object(javascript)
            if self.total_size==-1:
                self.total_size = int(data["mainInfo"]["totalResults"]) # 4080
            for product in data["mods"]["listItems"]:
                self.product_url_list.append(self.PROTOCOL + product["productUrl"])
            if(len(self.product_url_list)>0):
                for p_url in self.product_url_list[0:2]:
                    yield scrapy.Request(url =  p_url,callback = self.parse_item)
                    # "https://www.lazada.sg/products/prism-e65-4k-uhd-smart-digital-tv-hdr-zerobezel-design-4k-netflix-youtube-app-ips-panel-dolby-audio-digital-tv-ready-wifi-enabled-free-indoor-antenna-worth-35-i1010898153-s3698062714.html?search=1", callback = self.parse_item)
            self.current_size = self.current_size + 40  # because every page has 40 data
            self.page_no = self.page_no+1
            # print(self.product_url_list)
            # print(len(self.product_url_list))
            if(self.current_size<=self.total_size):
                next_page_url= f'https://www.lazada.sg/catalog/?_keyori=ss&from=input&page={self.page_no}&q=tv&sort=popularity'
                yield scrapy.Request(url = next_page_url, callback = self.parse)
        except:
            self.current_size = self.current_size + 40 
            self.page_no = self.page_no+1
            print("I dont want to be processed"+str(response.url))
            if(self.current_size<=self.total_size):
                next_page_url= f'https://www.lazada.sg/catalog/?_keyori=ss&from=input&page={self.page_no}&q=tv&sort=popularity'
                yield scrapy.Request(url = next_page_url, callback = self.parse)
            
    def parse_item(self,response):
        # with open("product_dummy.html","w+",encoding="utf-8") as fp:
        #     fp.write(response.text)
        script_css = 'script:contains("__moduleData__")::text'
        script_pattern = r'__moduleData__ = (.*);'
        # warning: for some pages you need to pass replace_entities=True
        # into re_first to have JSON escaped properly
        script_text = response.css(script_css).re_first(script_pattern,replace_entities=True)
        try:
            json_data = chompjs.parse_js_object(script_text)
            item_obj = scrap_product(json_data["data"]["root"],response.url)
            yield item_obj
        except ValueError as e:
            json_data = {}
            # this code is dependent on html structure an change in that will affect the code
            soup = BeautifulSoup(response.text, 'lxml')
            for data in soup.findAll("script"):
                if "__moduleData__" in str(data):
                    module_data = str(data).split("var __moduleData__ =")
                    for part in module_data:
                        if('{"data":{"root"' in part):
                            string_data = part.partition("var __googleBot__ =")[0].rsplit(";",1)
                            json_data = json.loads(string_data[0].strip())["data"]["root"]
                            break
            item_obj = scrap_product(json_data,response.url) 
            yield item_obj
        except:
            item_obj = LazadaCrawlerItem()
            item_obj["link"] = response.url
            yield item_obj
        

