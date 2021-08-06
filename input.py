import json
import os
from urllib.parse import urlparse

CONFIG_FILE_PATH = "config.json"
RESOURE_DIR = "resource"

class ConfigBox:
    def __init__(self):
        self.config = load_config()
        self.search_data = self.config["search_data"]
        self.total_size = self.config["total_size"]
        self.create_dir_structure()

    def create_dir_structure(self):
        for data in self.search_data:
            if(data["website"]):
                domain_name = urlparse(data["website"]).netloc
                if(domain_name):
                    os.makedirs(os.path.join(RESOURE_DIR, domain_name),exist_ok=True)
                    if(len(data["search_string"])>0):
                        for search_string in data["search_string"]:
                            os.makedirs(os.path.join(RESOURE_DIR, domain_name,search_string),exist_ok=True)

def load_config():
    config_data = {
        "search_data": [],
        "total_size": 0
    }
    with open(CONFIG_FILE_PATH) as fp:
        data = json.load(fp)
    config_data["search_data"] = data
    config_data["total_size"] = len(data)
    return config_data

ConfigBox()