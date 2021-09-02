from bs4 import BeautifulSoup
import json

file_data = ""

with open("E:\\scrap_world\\scrap_world\\lazada_crawler\\product_dummy.html","r",encoding="utf-8") as fp:
    file_data = fp.read()


soup = BeautifulSoup(file_data, 'lxml')
# print(soup.find('script', type='application/ld+json'))
for data in soup.findAll("script"):
    if "__moduleData__" in str(data):
        data1 = str(data).split("var __moduleData__ =")
        for d in data1:
            if('{"data":{"root"' in d):
                string_data = d.partition("var __googleBot__ =")[0].rsplit(";",1)
                print(json.loads(string_data[0].strip())["data"]["root"])

       


# # data_encode = file_data.encode(encoding='UTF-8',errors='backslashreplace')
# data_decode = file_data
# print(data_decode)