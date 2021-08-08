import requests
import json
import urllib
from item_obj import Item_Obj
import os
from concurrent.futures import ThreadPoolExecutor

MAX_THREADS = 10

# SEARCH_LINK = "https://shopee.sg/api/v4/search/search_items?by=relevancy&keyword=tv&limit=60&newest=0&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2"
# https://shopee.sg/api/v2/item/get?itemid={item_id}&shopid={shop_id}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
}

class ShopeeScraper():
    def __init__(self, website, domain_name, search_data):
        self.website = website
        self.domain_name =domain_name
        self.search_data = search_data
        self.scraped_items = []
        self.get_item_links()
       
    def get_item_links(self):
        for data in self.search_data:
            new_count = 0
            limit = 60
            total_count = 1
            session = requests.Session()
            # try:
            while new_count <= total_count:
                print("total count"+str(total_count))
                print("new count"+str(new_count))
                search_link = f"https://shopee.sg/api/v4/search/search_items?by=relevancy&keyword={data}&limit={limit}&newest={new_count}&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2"
                search_data = requests.get(search_link, headers=headers) # http request
                search_json_data = search_data.json()
                items_data = search_json_data["items"]
                total_count = search_json_data["total_count"]
                # first_item = items_data[0]
                # count = 0 
                item_url_list = [f'https://shopee.sg/api/v2/item/get?itemid={item["item_basic"]["itemid"]}&shopid={item["item_basic"]["shopid"]}' for item in items_data ]
                print(f'Under process url count {len(item_url_list)}')
                threads = min(MAX_THREADS, len(item_url_list))
                with ThreadPoolExecutor() as executor:
                    executor.map(self.scrap_item_data,item_url_list,items_data)
                new_count = new_count + 60
            item_data_json = self.scraped_items
            file_path = os.path.join("resource",self.domain_name,data)
            with open(file_path+'/item_data.json', 'w', encoding='utf-8') as fp:
                json.dump(item_data_json, fp, ensure_ascii=False, indent=4)
            self.scraped_items = []
        
    def scrap_item_data(self,item_link,item):
        # session = requests.Session()
        item_data = requests.get(item_link,headers=headers).json()
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
        self.scraped_items.append(item_object.__dict__)

    def scrape_name(self,item_data,item_object: Item_Obj):
        item_name = item_data["item"]["name"]
        item_object.set_name(item_name)
    
    def scrape_org_price(self,item_data,item_object:Item_Obj):
        try:
            item_minprice = str(item_data["item_basic"]["price_min_before_discount"]/100000)
        except:
            item_minprice = ""
        try:
            item_maxprice = str(item_data["item_basic"]["price_max_before_discount"]/100000)
        except:
            item_maxprice = ""
        item_object.set_org_price("-".join([item_minprice,item_maxprice]))

    def scrape_new_price(self,item_data,item_object: Item_Obj):
        try:
            item_price = str(item_data["item_basic"]["price"]/100000)
        except:
            item_price = ""
        try:
            item_minprice = str(item_data["item_basic"]["price_min"]/100000)
        except:
            item_minprice = ""
        try:
            item_maxprice = str(item_data["item_basic"]["price_max"]/100000)
        except:
            item_maxprice = ""
        item_object.set_new_price("-".join([item_minprice,item_maxprice]))
    
    def scrape_desc(self,item_data,item_object: Item_Obj):
        item_desc = item_data["item"]["description"]
        item_object.set_desc(item_desc)

    def scrape_brand(self,item_data,item_object: Item_Obj):
         item_brand = item_data["item"]["brand"]
         item_object.set_brand(item_brand)
    
    def scrape_discount(self,item_data,item_object: Item_Obj):
        item_discount = item_data["item"]["discount"]
        item_object.set_discount(item_discount)
    
    def scrape_rating(self,item_data,item_object: Item_Obj):
        item_rating = item_data["item_basic"]["item_rating"]["rating_star"]
        item_object.set_rating(item_rating)

    def scrape_categories(self,item_data,item_object: Item_Obj):
        bread_crumbs=[]
        for data in item_data["item"]["categories"]:
            bread_crumbs.append(data["display_name"])
        item_object.set_categories(" >> ".join(bread_crumbs))
