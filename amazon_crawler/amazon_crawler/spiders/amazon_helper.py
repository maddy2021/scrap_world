import scrapy
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from urllib.parse import urljoin
import re
import json
from scrapy import Selector
from urllib.parse import urlparse
import unicodedata


def scrap_book_price(selector):
    book_price = ""
    scrap_price = selector.xpath("//*[@id='soldByThirdParty']/span/text()").extract()
    if(len(scrap_price)>0):
        book_price = scrap_price[0]
    #for kindle books
    if(book_price == ""):
        scrab_probable_price_div = selector.xpath("//*[@id='buybox']/div/table").extract_first() or ""
        if scrab_probable_price_div:
            bs = BeautifulSoup(scrab_probable_price_div,features="lxml")
            book_price_list = bs.select("td.a-size-medium.a-color-price")
            if len(book_price_list) > 0:
                book_price = book_price_list[0].text
    if(book_price == ""):
        scrab_probable_price_div = selector.xpath("//*[@id='buyOneClick']/div[2]/table").extract_first()
        if scrab_probable_price_div:
            bs = BeautifulSoup(scrab_probable_price_div,features="lxml")
            book_price_list = bs.select("span.a-size-medium.a-color-price")
            if len(book_price_list) > 0:
                book_price = book_price_list[0].text
    return book_price

def get_original_book_price(selector):
    book_price = ""
    scrap_probable_part = selector.xpath("//div[@id='price']/table").extract_first() or ""
    if scrap_probable_part:
        bs = BeautifulSoup(scrap_probable_part,features="lxml")
        book_price_list = bs.select("span.priceBlockStrikePriceString.a-text-strike")
        if len(book_price_list) > 0:
            book_price = book_price_list[0].text
    scrap_price = selector.xpath("//*[@id='buyBoxInner']/ul/li[1]/span/span[2]/text()").extract()
    if(len(scrap_price)>0):
        book_price = scrap_price[0]
    #for kindle books
    if(book_price == ""):
        scrap_probable_price_div = selector.xpath("//*[@id='buybox']/div/table").extract_first() or ""
        if scrap_probable_price_div:
            bs = BeautifulSoup(scrap_probable_price_div,features="lxml")
            book_price_list = bs.select("span.a-color-secondary.a-text-strike")
            if len(book_price_list) > 0:
                book_price = book_price_list[0].text
    if(book_price == ""):
        scrap_probable_price_div = selector.xpath("//*[@id='buyOneClick']/div[2]/table").extract_first()
        if scrap_probable_price_div:
            bs = BeautifulSoup(scrap_probable_price_div,features="lxml")
            book_price_list = bs.select("span.a-color-secondary.a-text-strike")
            if len(book_price_list) > 0:
                book_price = book_price_list[0].text
    return book_price.strip()

def get_book_features(selector):
    raw_html = selector.xpath("//*[@id='detailBullets_feature_div']").extract_first()
    clean_text = ""
    if(raw_html!=""):
        soup = BeautifulSoup(raw_html, "html.parser") # create a new bs4 object from the html data loaded
        for script in soup(["script", "style"]): # remove all javascript and stylesheet code
            script.extract()
     
        clean_text = soup.get_text()
        if(clean_text):
            clean_text = re.sub("\\n+", "\\n", clean_text)
            clean_text = clean_text.replace("\n:\n"," : ").strip().replace(":\n"," : ").strip().replace("\n"," || ")
    return clean_text
        

def scrap_gift_card_price(selector):
    scrap_price = selector.xpath("//ul[@id='gc-amount-mini-picker']/li").extract()
    gift_card_price_list = []
    for idx,item in enumerate(scrap_price):
        bs = BeautifulSoup(item,features="lxml")
        if(bs):
            price_button = bs.find("button")
            if(price_button):
                gift_card_price_list.append(price_button.text.strip())
    return " || ".join(gift_card_price_list)

def scrap_navbar_as_breadcrumb(selector):
    bread_crumb = ""
    bread_crumb_list = []
    scrap_nav_bar = selector.xpath("//div[@id='nav-subnav']")
    if(scrap_nav_bar):
        bs = BeautifulSoup(scrap_nav_bar.extract_first(),features="lxml")
        nav_item_list = bs.findAll("span")
        for data in nav_item_list:
            bread_crumb_list.append(data.text.strip())
        if(len(bread_crumb_list)>0):
            bread_crumb = "=>".join([item for item in bread_crumb_list if item.strip()])
    return bread_crumb
