import time
import schedule
import requests
from server import Server
from loguru import logger
from proxy import ProxyScrapper
from sqliteconnector import SqliteConnector

class Scrapper():
    def __init__(self):
        try:
            logger.info("Initializing the Scrapper")
            self.connector = SqliteConnector()
            self.url = "https://www.whatsmydns.net/api/servers"
            self.connector.create_tables() #Init the Database
            self.proxies = ProxyScrapper().get_proxies() #Get list of 15 proxy servers
            self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        except Exception as e:
            logger.error("Failed to initialize the Scrapper: " + str(e))

    def scrap(self):
        try:
            self.SERVERS = []
            for proxy in self.proxies:
                logger.info("Looping proxy server to get WhatsMyDns servers")
                logger.info ("Using: " + proxy.ip + " Proxy server")
                proxies = {proxy.type : proxy.ip}
                logger.info("Getting list of servers from Whatsmydns API")
                servers = requests.get(self.url,proxies=proxies,headers=self.headers).json()
                for server in servers:
                    self.SERVERS.append(Server(
                    id=server['id'],
                    latitude=server['latitude'],
                    longitude=server['longitude'],
                    location=server['location'],
                    provider=server['provider'],
                    country=server['country'],
                )
                    )
            logger.info("Got total of " + str(len(self.SERVERS)) + " Before removing duplications")
            self.SERVERS =  remove_duplicates(self.SERVERS)
            logger.info("Got total of " + str(len(self.SERVERS)) + " After removing duplications")
            for server in self.SERVERS:
                self.connector.add_server(server.id, server.latitude,server.longitude,server.provider, server.location, server.country, server.status)
            logger.info("Total servers in database: " + str(len(scrapper.connector.get_active_servers())))
        except Exception as e:
            logger.error("Error Scrapping: " + str(e))
                
def remove_duplicates(servers):
    try:
        logger.info("Removing duplicate entries from the servers list")
        unique_servers = list(set(servers))
        return unique_servers
    except Exception as e:
        logger.error("Error removing duplicate entries from servers list: " + str(e))
        return servers


if __name__=="__main__":
    try:
        logger.info("Running...")
        scrapper = Scrapper()
        scrapper.scrap()
        logger.info("Adding to sechedule to run every 12 hours")
        schedule.every(12).hours.do(scrapper.scrap)

        logger.info("Running...")
        while True:
            schedule.run_pending()
            time.sleep(1)

    except Exception as e:
        logger.error("Error scrapping: " + str(e))
