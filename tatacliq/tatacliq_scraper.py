import requests
import json
import urllib
from .items import Item_Obj
import os
from concurrent.futures import ThreadPoolExecutor
import re
import xmltodict 

MAX_THREADS = 10

# SEARCH_LINK = "https://shopee.sg/api/v4/search/search_items?by=relevancy&keyword=tv&limit=60&newest=0&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2"
# https://shopee.sg/api/v2/item/get?itemid={item_id}&shopid={shop_id}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
}

class TataCliqScraper():
    def __init__(self, website, domain_name, search_data):
        self.website = website
        self.domain_name =domain_name
        self.search_data = search_data
        self.scraped_items = []
        self.get_item_links()
       
    def get_item_links(self):
        for data in self.search_data:
            new_count = 0
            # limit = 40
            total_count = 1000
            session = requests.Session()
            try:
                # https://prodsearch.tatacliq.com/products/mpl/search/?searchText={data}%3Arelevance%3AinStockFlag%3Atrue&isKeywordRedirect=false&isKeywordRedirectEnabled=true&channel=WEB&isMDE=true&isTextSearch=false&isFilter=false&qc=false&test=minimal.fields&page={pageno}&isPwa=true&pageSize=40&typeID=all
                while new_count <= total_count-1:
                    # try:
                    print("total count"+str(total_count))
                    print("new count"+str(new_count))
                    search_link = f"https://prodsearch.tatacliq.com/products/mpl/search/?searchText={data}%3Arelevance%3AinStockFlag%3Atrue&isKeywordRedirect=false&isKeywordRedirectEnabled=true&channel=WEB&isMDE=true&isTextSearch=false&isFilter=false&qc=false&test=minimal.fields&page={new_count}&isPwa=true&pageSize=40&typeID=all"
                    # search_link = f"https://shopee.sg/api/v4/search/search_items?by=relevancy&keyword={data}&limit={limit}&newest={new_count}&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2"
                    search_data = requests.get(search_link, headers=headers) # http request
                    search_json_data = search_data.json()
                    items_data = search_json_data["searchresult"]
                    total_count = search_json_data["pagination"]["totalPages"]
                    # first_item = items_data[0]
                    # count = 0 
                    # "https://"+ urlparse(response.url).netloc+"/marketplacewebservices/v2/mpl/products/productDetails/"+product_id+"?isPwa=true&isMDE=true"
                    # https://www.tatacliq.com/marketplacewebservices/v2/mpl/products/productDetails/mp000000005159814?isPwa=true&isMDE=true
                    item_url_list = [f'https://www.tatacliq.com/marketplacewebservices/v2/mpl/products/productDetails/{item["productId"]}?isPwa=true&isMDE=true' for item in items_data]
                    # item_url_list = [f'https://shopee.sg/api/v2/item/get?itemid={item["item_basic"]["itemid"]}&shopid={item["item_basic"]["shopid"]}' for item in items_data ]
                    print(f'Under process url count {len(item_url_list)}')
                    threads = min(MAX_THREADS, len(item_url_list))
                    with ThreadPoolExecutor() as executor:
                        executor.map(self.scrap_item_data,item_url_list,items_data)
                    new_count = new_count + 1
            except:
                new_count = new_count + 1
                pass
            item_data_json = self.scraped_items
            file_path = os.path.join("resource",self.domain_name,data)
            with open(file_path+'/item_data.json', 'w', encoding='utf-8') as fp:
                json.dump(item_data_json, fp, ensure_ascii=False, indent=4)
            self.scraped_items = []
        
    def scrap_item_data(self,item_link,item):
        # session = requests.Session()
        response = requests.get(item_link,headers=headers)
        item_data = {}
        # print(response.headers["Content-Type"])
        if("json" in response.headers["Content-Type"].lower()):
            item_data = json.loads(response.text)
        elif("xml" in response.headers["Content-Type"].lower()):
            data_dict = xmltodict.parse(response.text) 
            item_data = json.loads(json.dumps(data_dict))["mplNewProductDetailMobileWsData"]
        item_object = Item_Obj()
        item_object.set_link(item_link)
        self.scrape_name(item_data,item_object)
        self.scrape_desc(item_data,item_object)
        self.scrape_brand(item_data,item_object)
        self.scrape_discount(item_data,item_object)
        self.scrape_org_price(item,item_object)
        self.scrape_new_price(item,item_object)
        self.scrape_rating(item,item_object)
        self.scrape_categories(item_data,item_object) 
        self.scrape_features(item_data,item_object) 
        self.scraped_items.append(item_object.__dict__)

    def scrape_name(self,scrap_data_json,item_object: Item_Obj):
        product_name = ""
        try:
            if("productTitle" in scrap_data_json and "brandName" in scrap_data_json):
                product_name= scrap_data_json["productTitle"] + "("+scrap_data_json["brandName"]+ ")" 
            elif("productTitle" in scrap_data_json):
                product_name= scrap_data_json["productTitle"] + "("+scrap_data_json["brandName"]+ ")"
            item_object.set_name(product_name)
        except:
            item_object.set_name("")
        
    
    def scrape_org_price(self,scrap_data_json,item_object:Item_Obj):
        product_original_price = ""
        try:
            if("mrpPrice" in scrap_data_json):
                product_original_price= scrap_data_json["mrpPrice"]["commaFormattedValue"] 
            if product_original_price == "" and "price" in scrap_data_json:
                product_original_price = scrap_data_json["price"]["mrpPrice"]["commaFormattedValue"] 
        except:
            product_original_price = ""
        item_object.set_org_price(product_original_price)

    def scrape_new_price(self,scrap_data_json,item_object: Item_Obj):
        product_price = ""
        try:
            if("winningSellerPrice" in scrap_data_json):
                product_price= scrap_data_json["winningSellerPrice"]["commaFormattedValue"] 
            if product_price == "" and "price" in scrap_data_json:
                product_price = scrap_data_json["price"]["sellingPrice"]["commaFormattedValue"] 
        except:
            product_price = ""
        item_object.set_new_price(product_price)
    
    def scrape_desc(self,scrap_data_json,item_object: Item_Obj):
        product_description = ""
        try:
            if("productDescription" in scrap_data_json):
                product_description= scrap_data_json["productDescription"]
        except:
            product_description = ""
        item_object.set_desc(product_description)

    def scrape_features(self,scrap_data_json,item_object: Item_Obj):
        product_details_list = []
        try:
            if("details" in scrap_data_json):
                product_details = scrap_data_json["details"]
                if("entry" in product_details):
                    product_details = product_details["entry"]
                for data in product_details:
                    for key,value in data.items():
                        product_details_list.append(key+" : "+value)
        except:
            product_details_list = []
        item_object.set_features(" || ".join(product_details_list))

    def scrape_brand(self,scrap_data_json,item_object: Item_Obj):
        item_brand = ""
        if("brandName" in scrap_data_json):
            item_brand = scrap_data_json["brandName"]
        item_object.set_brand(item_brand)
    
    def scrape_discount(self,scrap_data_json,item_object: Item_Obj):
        item_discount = ""
        if("discount" in scrap_data_json):
            item_discount = str(scrap_data_json["discount"])
        item_object.set_discount(item_discount)
    
    def scrape_rating(self,scrap_data_json,item_object: Item_Obj):
        item_rating = ""
        if("averageRating" in scrap_data_json):
            item_rating = str(scrap_data_json["averageRating"])
        item_object.set_rating(item_rating)

    def scrape_categories(self,scrap_data_json,item_object: Item_Obj):
        bread_crumb_name_list = []
        try:
            if("seo" in scrap_data_json):
                bread_Crumb_data = scrap_data_json["seo"]["breadcrumbs"]
                bread_crumb_name_list = []
                for data in bread_Crumb_data:
                    bread_crumb_name_list.append(data["name"])
        except:
            bread_crumb_name_list = []
        item_object.set_categories(" >> ".join(bread_crumb_name_list))
