import scrapy
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from urllib.parse import urljoin
import re
import json
from scrapy import Selector
from ..items import FlipkartItem
from urllib.parse import urlparse
from scrapy.selector import Selector

# scrap product name 
def scrap_product_name(selector):
    data= selector.xpath('string(//div[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[1]/h1)').getall() or []
    data = list(filter(None, data))
    if(len(data)==0):
        data = selector.xpath('string(//span[contains (@class,"B_NuCI")])').getall()
    if len(data) >0 :
        return data[0].strip()
    return ""

# scrap product selling name
def scrap_product_price(selector):
    # data = selector.css('._3qQ9m1')
    data = selector.xpath('//div[contains (@class,"_3iZgFn")]') or selector.xpath('//div[contains (@class,"_25b18c")]') or ""
    if(data != ""):
        product_price = data.xpath("//div[@class='_1uv9Cb']//text()").get() or data.xpath("//div[@class='_30jeq3 _16Jk6d']//text()").get() or ""
        return product_price
    return ""

def scrap_product_original_price(selector):
    # data = selector.css('._3qQ9m1')
    data = selector.xpath('//div[contains (@class,"_3iZgFn")]') or selector.xpath('//div[contains (@class,"_25b18c")]') or ""
    if(data != ""):
        product_original_price = data.xpath("string(//div[@class='_3auQ3N _1POkHg'])").get() or data.xpath("string(//div[@class='_30jeq3 _16Jk6d'])").get() or ""
        return product_original_price
    return ""
    # return selector.xpath('string(//div[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[4]/div[1]/div/div[2])').get() or ""

# scrap product bread crumb
def scrap_bread_crumb(selector):
    bread_crumb_string = ""
    bread_crumb = selector.xpath('//div[@id="container"]/div/div[3]/div[1]/div[2]/div[1]/div[1]/div/div[@class="_3GIHBu"]/a//text()').extract() or []
    if(len(bread_crumb)>0):
        bread_crumb_string = "=>".join(bread_crumb)
    if(bread_crumb_string!=""):
        current_bread_crumb = selector.xpath('//div[@id="container"]/div/div[3]/div[1]/div[2]/div[1]/div[1]/div/div[@class="_3GIHBu"]/div/div/p//text()').get() or ""
        bread_crumb_string = bread_crumb_string + "=>" + current_bread_crumb
    return bread_crumb_string

# scrap product description
def scrap_product_description(selector):
    product_description_string = ""
    product_description_list = []
    data = selector.xpath('//div[@class="_3gijNv col-12-12"]/div[contains (@class,"_38NXIU")]').extract() or []
    if(data!=[]):
        for item in data:
            bs = BeautifulSoup(item,features="lxml")
            key = bs.find("div",  {"class":"_2THx53"})
            value = bs.find("p")
            if(key!="" and value!=""):
                product_description_list.append(key.text + " : " + value.text)
        if len(product_description_list)>0:
            product_description_string = " || ".join([item.strip() for item in product_description_list if item.strip()])
    if(product_description_string == ""):
        data = selector.xpath('//div[@class="_3gijNv col-12-12"]/div[contains (@class,"_1y9a40")]//text()').getall() or []
        if(len(data)>0):
            product_description_string = " || ".join([item.strip() for item in data if item.strip()])
    return product_description_string

# scrap product features (To table view)
def scrap_product_rating(selector):
    # product_specification_list = []
    # product_specification_string = ""
    rating_string = ""
    try:
        #data = selector.xpath('//div[@id="container"]/div/div[3]/div[1]/div[2]/div[@class="ooJZfD _2oZ8XT"]/div[@class="_3gijNv col-12-12"]/div[@class="MocXoX"]').extract_first() or ""
        # data = selector.xpath('//div[@class="_3gijNv col-12-12"]/div[@class="MocXoX"]').extract_first() or selector.xpath('//div[@class="_1AtVbE col-12-12"]/div[@class="_3dtsli"]').extract_first() or ""
        # if(data != ""):
        #     bs = BeautifulSoup(data,features='lxml')
        #     tables = bs.findAll('table')
        #     if(len(tables)>0):
        #         for table in tables:
        #             key_list = table.select("td._3-wDH3.col.col-3-12") or table.select("td._1hKmbr.col.col-3-12")
        #             value_list = table.select('td._2k4JXJ.col.col-9-12') or table.select("td.URwL2w.col.col-9-12")
        #             for item in list(zip(key_list,value_list)):
        #                 # print(item)
        #                 key = item[0].text or ""
        #                 value = ""
        #                 value_list = item[1].findAll('li')
        #                 if(len(value_list)>0):
        #                     value = " => ".join([list_item.text for list_item in value_list])
        #                 # print(key+" : "+value)
        #                 if(key!="" and value!=""):
        #                     product_specification_list.append(key + " : "+value)
        # # when features in drop down based product description
        # if(product_specification_string==""):
        #     feature_data_html = selector.xpath('//div[@class="_2GNeiG"]/div[@class="row"]').extract() or []
        #     print(len(feature_data_html))
        #     for item in feature_data_html:
        #         if(item):
        #             bs = BeautifulSoup(item,features='lxml')
        #             key = bs.find("div",class_="col col-3-12 _1kyh2f").get_text() or ""
        #             value = bs.find("div",class_="col col-9-12 _1BMpvA").get_text() or ""
        #             if(key or value):
        #                 product_specification_list.append(key.strip()+ " : " +value.strip())
        # if(len(product_specification_list)>0):
        #     product_specification_string = " || ".join(product_specification_list) _2e3Uck _2_0QCf
        # #   row _1UjZpa
        rating_string_list = selector.xpath("//div[@class='gUuXy- gP6o01 _1eJXd3']//text()").getall() or []
        if(len(rating_string_list)==0):
            rating_string_list = selector.xpath("//div[@class='_2e3Uck _2_0QCf']//text()").getall() or []
        if(len(rating_string_list)==0):
            #row _3AjFsn _2c2kV-
            rating_string_list = selector.xpath("//div[@class='_2e3Uck']//text()").getall()
        if(len(rating_string_list)>0):
            rating_string =" || ".join(item.strip() for item in rating_string_list if item.strip())
        return rating_string
    except:
        return ""


# # scrap product features (To table view)
def scrap_product_features(selector):
    product_specification_list = []
    product_specification_string = ""
    rating_string = ""
    try:
        #data = selector.xpath('//div[@id="container"]/div/div[3]/div[1]/div[2]/div[@class="ooJZfD _2oZ8XT"]/div[@class="_3gijNv col-12-12"]/div[@class="MocXoX"]').extract_first() or ""
        data = selector.xpath('//div[@class="_3gijNv col-12-12"]/div[@class="MocXoX"]').extract_first() or selector.xpath('//div[@class="_1AtVbE col-12-12"]/div[@class="_3dtsli"]').extract_first() or ""
        if(data != ""):
            bs = BeautifulSoup(data,features='lxml')
            tables = bs.findAll('table')
            if(len(tables)>0):
                for table in tables:
                    key_list = table.select("td._3-wDH3.col.col-3-12") or table.select("td._1hKmbr.col.col-3-12")
                    value_list = table.select('td._2k4JXJ.col.col-9-12') or table.select("td.URwL2w.col.col-9-12")
                    for item in list(zip(key_list,value_list)):
                        # print(item)
                        key = item[0].text or ""
                        value = ""
                        value_list = item[1].findAll('li')
                        if(len(value_list)>0):
                            value = " => ".join([list_item.text for list_item in value_list])
                        # print(key+" : "+value)
                        if(key!="" and value!=""):
                            product_specification_list.append(key + " : "+value)
        # when features in drop down based product description
        if(product_specification_string==""):
            feature_data_html = selector.xpath('//div[@class="_2GNeiG"]/div[@class="row"]').extract() or []
            print(len(feature_data_html))
            for item in feature_data_html:
                if(item):
                    bs = BeautifulSoup(item,features='lxml')
                    key = bs.find("div",class_="col col-3-12 _1kyh2f").get_text() or ""
                    value = bs.find("div",class_="col col-9-12 _1BMpvA").get_text() or ""
                    if(key or value):
                        product_specification_list.append(key.strip()+ " : " +value.strip())
        # when features in drop down based product description
        if(product_specification_string==""):
            feature_data_html = selector.xpath('//div[@class="X3BRps"]/div[@class="row"]').extract() or []
            print(len(feature_data_html))
            for item in feature_data_html:
                if(item):
                    bs = BeautifulSoup(item,features='lxml')
                    key = bs.find("div",class_="col col-3-12 _2H87wv").get_text() or ""
                    value = bs.find("div",class_="col col-9-12 _2vZqPX").get_text() or ""
                    if(key or value):
                        product_specification_list.append(key.strip()+ " : " +value.strip())
        if(product_specification_string==""):
            feature_data_html = selector.xpath('//div[@class="X3BRps _13swYk"]/div[@class="row"]').extract() or []
            print(len(feature_data_html))
            for item in feature_data_html:
                if(item):
                    bs = BeautifulSoup(item,features='lxml')
                    key = bs.find("div",class_="col col-3-12 _2H87wv").get_text() or ""
                    value = bs.find("div",class_="col col-9-12 _2vZqPX").get_text() or ""
                    if(key or value):
                        product_specification_list.append(key.strip()+ " : " +value.strip())
        if(len(product_specification_list)>0):
            product_specification_string = " || ".join(product_specification_list)
        # #   row _1UjZpa
        # rating_string_list = selector.xpath("//div[@class='_3ors59']//text()").getall() or []
        # if(len(rating_string_list)>0):
        #     rating_string =" || "+" || ".join(item.strip() for item in rating_string_list if item.strip())
        return product_specification_string
    except:
        return ""


def scrap_seller_details(selector):
    seller_details = ""
    seller_id_text = "none"
    seller_rating = "none"
    policy_info_text = "none"
    try:
        data_list = selector.xpath('//div[contains (@class,"_1AtVbE col-12-12")]').extract() or []
        # is seller id present ?
        if(data_list!=[]):
            for data in data_list:
                seller_id = Selector(text=data).xpath('//*[@id="sellerName"]')
                if(seller_id):
                    soup =  BeautifulSoup(data,features="lxml")
                    seller_id_text = soup.find("div", {"id": "sellerName"}).get_text() or "none"
                    seller_rating = seller_rating = seller_id.xpath('//div[contains (@class,"_3LWZlK")]//text()').get() or "none"    
                    #soup.find("div", {"class": "_3LWZlK"}) or "none"
                    if(not seller_rating or seller_rating=="none"):
                        seller_rating = seller_id.xpath('//div[contains (@class,"_2Trmwm")]//text()').get() or ""
                        # soup.find("div", {"class": "_2Trmwm"}) or "none"    
                    policy_info = soup.find_all("li") or []
                    if(policy_info!=[]):
                        policy_info_text = " | ".join(element.get_text().strip() for element in policy_info)  
        seller_details = f'seller_id : {seller_id_text.replace(seller_rating,"").strip()} || seller_rating : {seller_rating.strip()} || extra_info : {policy_info_text}'
        return seller_details
    except:
        return ""

def scrap_highlights(selector):
    highlights = []
    hightlights_text = ""
    element_highlight = ""
    try :
        probable_highlights = selector.xpath('//div[contains (@class,"_1AtVbE col-6-12")]').extract() or []
        for highlights in probable_highlights:
            if(highlights):
                soup = BeautifulSoup(highlights,features='lxml')
                if("highlights" in soup.getText().lower()):
                    element_highlight = soup
        if(element_highlight):
            highlights = element_highlight.findAll("li") or []
        if(highlights):
            hightlights_text = " || ".join(highlight.get_text().strip() for highlight in highlights)
        return hightlights_text
    except:
        return ""
    
def scrap_flipkart_items(response):
    items = FlipkartItem()
    sel = Selector(response)
    # product details
    product_name = scrap_product_name(sel)
    product_price = scrap_product_price(sel)
    product_original_price = scrap_product_original_price(sel)
    bread_crumb = scrap_bread_crumb(sel)
    product_rating = scrap_product_rating(sel)
    product_feautures = scrap_product_features(sel)
    seller_details = scrap_seller_details(sel)
    highlights = scrap_highlights(sel)

    # # provide data to object for csv or json
    items['product_name'] = product_name
    items['product_price'] = product_price
    items['product_original_price'] = product_original_price
    items['bread_crumb'] = bread_crumb
    items['product_rating'] = product_rating
    items['product_features'] = product_feautures
    items['product_link'] = response.url
    items["seller_details"] = seller_details
    items["highlights"] = highlights
    items['domain_name'] = urlparse(response.url).netloc
    return items