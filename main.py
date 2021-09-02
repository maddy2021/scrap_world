from input import ConfigBox
from static import Domain
from shopee_scraper import ShopeeScraper
from tatacliq.tatacliq_scraper import TataCliqScraper
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from lazada_crawler.lazada_crawler.spiders.lazada import LazadaSpider
from flipkart.flipkart.spiders.flipkart_spider import FlipkartSpiderSpider
import scrapy
from scrapy.crawler import CrawlerProcess
import pathlib
import os

configuration = ConfigBox() # create directory 
for data in configuration.search_data:
    if(Domain.tatacliq.value in data["website"]):
        tatacliqObj = TataCliqScraper(data["website"],Domain.tatacliq.value,data["search_string"])
        pass
#     # if(Domain.SHOPEE_SG.value in data["website"]):
#     #     # shopeeScraperObj = ShopeeScraper(data["website"],Domain.SHOPEE_SG.value,data["search_string"])
#     #     pass
#     # elif(Domain.LAZADA_SG.value in data["website"]):
#     #     # Search site : https://www.lazada.sg/catalog/?_keyori=ss&from=input&page=1&q=tv&sort=popularity
          
#     #     process = CrawlerProcess(get_project_settings())

#     #     process.crawl(LazadaSpider,start_urls=['https://www.lazada.sg/catalog/?_keyori=ss&from=input&page=1&q=baby+toys&sort=popularity'])
#     #     process.start() # the script will block here until the crawling is finished
#     #     pass
#     #     #do some work
    # if(Domain.FLIPKART_COM.value in data["website"]):
    #     # Search site : https://www.lazada.sg/catalog/?_keyori=ss&from=input&page=1&q=tv&sort=popularity
    #     try:
    #         output_path = os.path.join("resource",data["website"],"item_data")
    #         url_list = []
    #         for item in data["search_string"]:
    #                 url_list.append(f"https://www.flipkart.com/search?q={item}&as-show=on&as-pos=2&as-type=RECENT")
    #         process = CrawlerProcess(settings={
    #             "FEED_EXPORTERS" : {
    #             'xlsx': 'scrapy_xlsx.XlsxItemExporter',
    #             },
    #             "FEEDS": {
    #                 pathlib.Path(output_path+'.xlsx') : {"format": "xlsx"},
    #             },
    #             "CONCURRENT_REQUESTS": 4,
    #             "DOWNLOAD_DELAY" : 0.25,
    #             "DEFAULT_REQUEST_HEADERS" : {
    #                 'Accept': 'text/plain,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #                 'Accept-Language': 'en',
    #                 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    #             },
    #             "HTTPERROR_ALLOW_ALL" : True,
    #         })

    #         process.crawl(FlipkartSpiderSpider,start_urls=url_list)
    #         process.start() # the script will block here until the crawling is finished
    #     except:
    #         pass