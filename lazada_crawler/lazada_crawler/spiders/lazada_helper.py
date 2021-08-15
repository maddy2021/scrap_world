from ..items import LazadaCrawlerItem

def scrape_name(item_data):
    product_name = item_data["fields"]["product"]["title"]
    return product_name

def scrape_org_price(item_data):
    pass

def scrape_new_price(item_data):
    pass

def scrape_desc(item_data):
    pass

def scrape_brand(item_data):
    pass

def scrape_discount(item_data):
    pass

def scrape_rating(item_data):
    pass

def scrape_categories(item_data):
    pass

def scrap_product(item_data):
    item_obj = LazadaCrawlerItem()
    item_obj["name"] = scrape_name(item_data)
    return item_obj
