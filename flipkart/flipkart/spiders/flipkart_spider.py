import scrapy
from ..items import FlipkartItem
from urllib.parse import urlparse
from .flipkart_helper import scrap_flipkart_items

class FlipkartSpiderSpider(scrapy.Spider):
    name = 'flipkart_spider'
    product_url_list = []
    start_urls = ['https://www.flipkart.com/search?q=tv&as-show=on&as-pos=2&as-type=RECENT']
    beggining_flag = False

    def parse(self, response):
        # self.page_no += 1

        products = response.xpath("//a[@class='_1fQZEK']").xpath("@href").getall()
        # //div[@class='_1AtVbE col-12-12']/div[@class='_13oc-S']/div/div[@class='_2kHMtA']/a[@class='_1fQZEK'] : Big link if needed
        if(len(products)==0):
            products = response.xpath("//a[@class='_2UzuFa']").xpath("@href").getall()
            
        for product in products:
            product_url = response.urljoin(product)
            yield scrapy.Request(url = product_url, callback = self.parse_laptop)
    
        probable_next_page_urls = response.xpath("//a[@class='_1LKTO3']").xpath("@href").getall()
        if(len(probable_next_page_urls)==2 and self.beggining_flag==True):
            next_page_url = response.urljoin(probable_next_page_urls[1])
            yield scrapy.Request(url = next_page_url, callback = self.parse)
        elif(len(probable_next_page_urls)==1 and self.beggining_flag==False):
            next_page_url = response.urljoin(probable_next_page_urls[0])
            self.beggining_flag = True
            yield scrapy.Request(url = next_page_url, callback = self.parse)    
        

    def parse_laptop(self, response):
        try:
            scraped_items = scrap_flipkart_items(response)
            # scraped_items["url_is_valid"] = True
        except:
            scraped_items = FlipkartItem()
            scraped_items['product_link'] = response.url
            scraped_items['domain_name'] = urlparse(response.url).netloc
            # scraped_items["url_is_valid"] = False
            scraped_items["status_code"] = str(response.status)
        yield scraped_items
