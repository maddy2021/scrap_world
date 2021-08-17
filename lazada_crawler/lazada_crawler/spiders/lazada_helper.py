from ..items import LazadaCrawlerItem
from scrapy import Selector

def scrape_name(item_data):
    try:
        product_name = item_data["fields"]["product"]["title"]
        return product_name
    except:
        return ""

def scrape_org_price(item_data):
    try:
        org_price = item_data["price"]["originalPrice"]["text"]
        return org_price
    except:
        return ""

def scrape_new_price(item_data):
    try:
        new_price = item_data["price"]["salePrice"]["text"]
        return new_price
    except:
        return ""

def scrape_desc(item_data):
    product_desc = ""
    try:
        if("desc" in item_data["fields"]["product"]):
            product_desc_selector = Selector(text=item_data["fields"]["product"]["desc"]) 
            product_desc_list = product_desc_selector.xpath("//span/text()").extract()
            if(len(product_desc_list)>0):
                product_desc = " || ".join([desc.strip() for desc in product_desc_list if desc.strip()!=""])
            if(product_desc==""):
                product_desc_list = product_desc_selector.xpath("//div/text()").extract()
                if(len(product_desc_list)>0):
                    product_desc = " || ".join([desc.strip() for desc in product_desc_list if desc.strip()!=""])
        if(product_desc==""):
            if("highlights" in item_data["fields"]["product"]):
                product_desc_selector = Selector(text=item_data["fields"]["product"]["highlights"])
                product_desc_list = product_desc_selector.xpath("//li/text()").extract()
                if(len(product_desc_list)>0):
                    product_desc = " || ".join([desc.strip() for desc in product_desc_list if desc.strip()!=""])
    except:
        product_desc = ""
    return product_desc

def scrape_brand(item_data):
    try:
        brand = item_data["fields"]["product"]["brand"]["name"]
        return brand
    except:
        return ""

def scrape_discount(item_data):
    try:
        discount = item_data["price"]["discount"]
        return discount
    except:
        return ""

def scrape_rating(item_data):
    try:
        rating = item_data["fields"]["review"]["ratings"]["average"]
        review_count = item_data["fields"]["review"]["ratings"]["reviewCount"]
        return str(rating) + "||" + str(review_count)
    except:
        return ""

def scrape_categories(item_data):
    try:
        bread_crum = []
        for obj in  item_data["fields"]["Breadcrumb"]:
            bread_crum.append(obj["title"])
        return " >> ".join(bread_crum)
    except:
        return ""

def scrape_specifications(item_data,sku_id):
    try:
        specification = item_data["fields"]["specifications"][sku_id]["features"]
    except:
        specification = ""
    return specification

def scrap_product(item_data, url):
    sku_id = item_data["fields"]["primaryKey"]["skuId"]
    sku_data = item_data["fields"]["skuInfos"][sku_id]
    item_obj = LazadaCrawlerItem()
    item_obj["name"] = scrape_name(item_data)
    item_obj["brand"] = scrape_brand(item_data)
    item_obj["desc"] = scrape_desc(item_data)
    item_obj["spec"] = scrape_specifications(item_data,sku_id)
    item_obj["discount"] = scrape_discount(sku_data)
    item_obj["org_price"] = scrape_org_price(sku_data)
    item_obj["new_price"] = scrape_new_price(sku_data)
    item_obj["rating"] = scrape_rating(item_data)
    item_obj["categories"] = scrape_categories(item_data)
    item_obj["link"] = url
    return item_obj
