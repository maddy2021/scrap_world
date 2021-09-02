import scrapy
from ..items import AmazonCrawlerItem
from urllib.parse import urlparse
from .scrape_amazon import scrape_amazon_items

class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    start_urls = ['https://www.amazon.in/s?k=refrigerator&ref=nb_sb_noss_2']
    count = 1

    def parse(self, response):
        # //div[contains(@class,'s-result-item s-asin')]//h2/a
        products = response.xpath("//div[contains(@class,'s-result-item s-asin')]//h2/a").xpath("@href").getall()
        for product in products:
            product_url = response.urljoin(product)
            yield scrapy.Request(url = product_url, callback = self.parse_product)
 
        probable_next_page_urls = response.xpath("//a[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator']")
        if(probable_next_page_urls):
            product_next_page = probable_next_page_urls.xpath('@href').get()
            next_page_url = response.urljoin(product_next_page)
            self.count = self.count+1
            yield scrapy.Request(url = next_page_url, callback = self.parse)
        # if(len(probable_next_page_urls)==2 and self.beggining_flag==True):
        #     next_page_url = response.urljoin(probable_next_page_urls[1])
        #     yield scrapy.Request(url = next_page_url, callback = self.parse)
        # elif(len(probable_next_page_urls)==1 and self.beggining_flag==False):
        #     next_page_url = response.urljoin(probable_next_page_urls[0])
        #     self.beggining_flag = True
        #     yield scrapy.Request(url = next_page_url, callback = self.parse) 
    
    def parse_product(self, response):
        try:
            scraped_items = scrape_amazon_items(response)
            # scraped_items["url_is_valid"] = True
        except:
            scraped_items = AmazonCrawlerItem()
            scraped_items['product_link'] = response.url
            scraped_items['domain_name'] = urlparse(response.url).netloc
            # scraped_items["url_is_valid"] = False
            scraped_items["status_code"] = str(response.status)
        yield scraped_items

