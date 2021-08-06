import requests
import json
import urllib
from item_obj import Item_Obj
import os

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
            search_link = f"https://shopee.sg/api/v4/search/search_items?by=relevancy&keyword={data}&limit=60&newest=0&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2"
            search_data = requests.get(search_link, headers=headers) # http request
            search_json_data = search_data.json()
            items_data = search_json_data["items"]
            # first_item = items_data[0]
            count = 0
            for item in items_data:
                if(count<3):
                    print("processing count:"+str(count))
                    shop_id = item["item_basic"]["shopid"]
                    item_id = item["item_basic"]["itemid"]
                    item_link = f"https://shopee.sg/api/v2/item/get?itemid={item_id}&shopid={shop_id}"
                    item_object = Item_Obj()
                    item_object.set_link(item_link)
                    self.scrap_item_data(item_link,item_object)
                    self.scraped_items.append(item_object.__dict__)
                    count = count + 1
            item_data_json = self.scraped_items
            file_path = os.path.join("resource",self.domain_name,data)
            with open(file_path+'/item_data.json', 'w', encoding='utf-8') as fp:
                json.dump(item_data_json, fp, ensure_ascii=False, indent=4)
            self.scraped_items = []



    def scrap_item_data(self,item_link,item_object: Item_Obj):
        item_data = requests.get(item_link,headers=headers).json()
        self.scrape_name(item_data,item_object)
        self.scrape_desc(item_data,item_object)
        self.scrape_brand(item_data,item_object)
        self.scrape_discount(item_data,item_object)
    

    def scrape_name(self,item_data,item_object: Item_Obj):
        item_name = item_data["item"]["name"]
        item_object.set_name(item_name)
    
    # def scrape_link(self,item_data,item_object):
    #     self.link = link

    # def scrape_org_price(self,item_data,item_object):
    #     item_price = item_data["item"][""]
    #     self.org_price = org_price

    # def scrape_new_price(self,item_data,item_object):
    #     self.new_price = new_price
    
    def scrape_desc(self,item_data,item_object: Item_Obj):
        item_desc = item_data["item"]["description"]
        item_object.set_desc(item_desc)

    def scrape_brand(self,item_data,item_object: Item_Obj):
         item_brand = item_data["item"]["brand"]
         item_object.set_brand(item_brand)
    
    def scrape_discount(self,item_data,item_object: Item_Obj):
        item_discount = item_data["item"]["discount"]
        item_object.set_discount(item_discount)
        

        




    