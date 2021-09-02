import scrapy
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from urllib.parse import urljoin
import re
import json
from scrapy import Selector
from ..items import AmazonCrawlerItem
from urllib.parse import urlparse
from . import amazon_helper
import unicodedata


# scrap product name 
def scrap_product_name(selector):
    product_name= selector.xpath("//span[@id='productTitle']//text()").get() or \
                    selector.xpath("//h1[@id='title']//text()").get() or \
                    selector.xpath("//span[@id='gc-asin-title']//text()").get() or\
                    ""
    if(product_name!=""):
        return product_name.strip()
    return product_name

# scrap product selling name
def scrap_product_price(selector):
    price = selector.xpath("//span[@id='priceblock_ourprice']//text()").get() or ""
    if(price == ""):
        price = selector.xpath("//span[@id='priceblock_dealprice']//text()").get() or ""
    if(price == ""):
        price = selector.xpath("//span[@id='priceblock_saleprice']//text()").get() or ""
    # for amazon books
    if(price == ""):
        price = amazon_helper.scrap_book_price(selector)
    #gift card
    if(price == ""):
        price = amazon_helper.scrap_gift_card_price(selector)
    # check this last in this function for availability 
    if(price == ""):
        price = selector.xpath("string(//div[@id='availability'])").get()
    if(price != ""):
        return price.replace("\n","").strip()
    return price

def scrap_product_original_price(selector):
    # code for books wanna check for all
    org_price = amazon_helper.get_original_book_price(selector)
    # original_price = amazon_helper.get_original_book_price(selector)
    return org_price

# scrap product bread crumb
def scrap_bread_crumb(selector):
    current_bread_crumb = ""
    bread_crumb = ""
    bread_crumb_list = selector.xpath("//div[@id='wayfinding-breadcrumbs_feature_div']/ul/li/span/a//text()").extract() or []
    if(bread_crumb_list != []):
        bread_crumb =  "=>".join([item.strip() for item in bread_crumb_list])
    if len(bread_crumb_list)>0:
        current_bread_crumb = selector.xpath("//div[@id='wayfinding-breadcrumbs_feature_div']/ul/li/span//text()").extract()[-1].strip()
    if(bread_crumb!=""):
        bread_crumb = bread_crumb+"=>"+current_bread_crumb
    # at the end if bread crumb is null scrap navbar (id : nav-subnav)
    if(bread_crumb == ""):
        bread_crumb = amazon_helper.scrap_navbar_as_breadcrumb(selector)
    return bread_crumb

# scrap product description
def scrap_product_description(selector):
    product_description = "==".join([item.strip() for item in selector.xpath("//div[@id='productDescription']/p//text()").getall()]) or ""
    # for books
    if(product_description == ""):
        raw_html = selector.xpath("//*[@id='editorialReviews_feature_div']/div[2]")
        if(raw_html):
            raw_html = raw_html.extract_first()
            cleanr = re.compile('<.*?>')
            cleantext = re.sub(cleanr, '', raw_html)
            cleantext = re.sub("\\n+", " || ", cleantext)
            product_description = unicodedata.normalize('NFD', cleantext).encode('utf-8').decode('utf-8')
    #gift card
    if(product_description == ""):
        gift_card_description_list = selector.xpath("//ul[@class='a-unordered-list a-vertical a-spacing-small']/li/span/text()").extract() or []
        if(len(gift_card_description_list)>0):
            product_description = " || ".join(item.strip() for item in gift_card_description_list if item.strip())
    return product_description

# scrap product features (To table view)
def scrap_product_features(selector):
    product_features_selector = selector.xpath("//div[@id='prodDetails']")
    info_array = []
    try:
        if(product_features_selector):
            bs = BeautifulSoup(product_features_selector.extract_first(),features="lxml")
            info_array = []
            # print(len(bs.findAll('table')))
            # if(len(bs.findAll('table'))>=2):
            tech_feature_table_key= product_features_selector.xpath("//table[@id='productDetails_techSpec_section_1']/tr/th//text()").extract() or []
            tech_feture_table_value= product_features_selector.xpath("//table[@id='productDetails_techSpec_section_1']/tr/td//text()").extract() or []
            if(len(tech_feature_table_key)>0 and len(tech_feture_table_value)>0):
                for key,value in zip([item.strip() for item in tech_feature_table_key],[item.strip() for item in tech_feture_table_value]):
                    info_array.append(key+ " : " +value)
                
            additional_feature_key = product_features_selector.xpath("//table[@id='productDetails_detailBullets_sections1']/tr/th//text()").extract() or []
            additional_feature_value = []
            additional_feature_raws = BeautifulSoup(product_features_selector.xpath("//table[@id='productDetails_detailBullets_sections1']").get(),features="lxml").findAll("td")
            for data in additional_feature_raws:
                additional_feature_value.append(data.text.strip().replace("\n","")) 
            if(len(additional_feature_key)>0 and len(additional_feature_value)>0):    
                for key,value in zip([item.strip() for item in additional_feature_key],[item.strip() for item in additional_feature_value if item.strip()]):
                    info_array.append(key+ " : " +value)
        if(len(info_array)==0):
            return amazon_helper.get_book_features(selector)
        return (" || ").join(info_array)
    except:
        return (" || ").join(info_array)


def get_rating(response):
    raw_html = response.xpath("//div[@id='detailBulletsWrapper_feature_div']").extract_first() or ""
    cleantext = ""
    if(raw_html != ""):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        cleantext = re.sub("\\n+", " || ", cleantext)
        cleantext = unicodedata.normalize('NFD', cleantext).encode('utf-8').decode('utf-8')
    return cleantext.strip()

def scrap_rating(response):
    rating_html =  response.xpath('//div[@class="a-section a-spacing-none a-spacing-top-mini cr-widget-ACR"]/div').extract() or []
    rating_data = []
    if len(rating_html)>0:
        for data in rating_html:
            bs = BeautifulSoup(data,features="lxml")
            rating_data.append(bs.get_text().strip())
    # print(rating_html)
    return " || ".join(rating_data)

def scrape_amazon_items(response):
    items = AmazonCrawlerItem()
    sel = Selector(response)
    # product details
    product_name = scrap_product_name(sel)
    product_price = scrap_product_price(sel)
    product_original_price = scrap_product_original_price(sel)
    bread_crumb = scrap_bread_crumb(sel)
    product_description = scrap_product_description(sel)
    product_feautures = scrap_product_features(sel)
    product_rating = scrap_rating(sel)

    # provide data to object for csv or json
    items['product_name'] = product_name
    items['product_price'] = product_price
    items['product_original_price'] = product_original_price
    items['bread_crumb'] = bread_crumb
    items['product_description'] = product_description
    items['product_features'] = product_feautures
    items['product_rating'] = product_rating
    items['product_link'] = response.url
    items['domain_name'] = urlparse(response.url).netloc
    return items