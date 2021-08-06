from input import ConfigBox
from static import Domain
from shopee_scraper import ShopeeScraper

configuration = ConfigBox() # create directory 

for data in configuration.search_data:
    if(Domain.SHOPEE_SG.value in data["website"]):
        shopeeScraperObj = ShopeeScraper(data["website"],Domain.SHOPEE_SG.value,data["search_string"])
        pass
    elif(Domain.LAZADA_SG.value in data["website"]):
        pass
        #do some work