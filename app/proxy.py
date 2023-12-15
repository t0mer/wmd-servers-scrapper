import requests
from loguru import logger
class Proxy():
    type:str
    anonymity:int
    country:str
    ip: str

    def __init__(self,type:str,anonymity:int,country:str,ip:str):
        self.type = type
        self.anonymity = anonymity
        self.country = country
        self.ip = ip


class ProxyScrapper():
    
    def __init__(self):
        self.proxies = []
        self.proxies_url = "https://api.proxyscrape.com/proxytable.php?nf=true&country=all"

    def get_proxies(self):
        try:
            proxy_list = requests.get(self.proxies_url)
            proxies_count = 0
            for ip, info in proxy_list.json()['http'].items():
                if proxies_count >= 15:
                    break
                anonymity = info.get('anonymity')
                country = info.get('country')
                self.proxies.append(Proxy(type="http",anonymity=anonymity,country=country,ip=ip))
                proxies_count +=1
            return self.proxies
        except Exception as e:
            logger.error("Error getting proxies. " + str(e))
            return []
        
if __name__ == "__main__":
    scrapper = ProxyScrapper()
    proxy = scrapper.get_proxies()[0]
   

       