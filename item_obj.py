class Item_Obj():
    def __init__(self, name="", link="", org_price="", new_price="", desc="",brand="",discount="",rating=""):
        self.name = name
        self. link = link
        self.org_price = org_price
        self.new_price = new_price
        self.desc = desc
        self.brand = brand
        self.discount = discount
        self.rating = rating

    def set_name(self,name):
        self.name = name
    
    def set_link(self,link):
        self.link = link

    def set_org_price(self,org_price):
        self.org_price = org_price

    def set_new_price(self,new_price):
        self.new_price = new_price
    
    def set_desc(self,desc):
        self.desc = desc

    def set_brand(self,brand):
        self.brand = brand
    
    def set_discount(self,discount):
        self.discount = discount

    def set_rating(self,rating):
        self.rating = rating