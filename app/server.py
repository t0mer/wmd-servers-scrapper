import uvicorn
from loguru import logger
from fastapi.responses import JSONResponse
from sqliteconnector import SqliteConnector
from fastapi import FastAPI, Request

class Server:
    def __init__(self):
        self.connector = SqliteConnector()

        self.tags_metadata = [
            {
                "name": "servers",
                "description": "Get servers list",
            },
        ]

        self.app = FastAPI(title="WhatsMyDNS servers", description="Get list of WhatmyDNS servers", version='1.0.0', openapi_tags=self.tags_metadata, contact={"name": "Tomer Klein", "email": "tomer.klein@gmail.com", "url": "https://github.com/t0mer/wmd-servers-scrapper"})

        @self.app.get("/get/servers",tags=['servers'], summary="Get list of servers")
        def get_servers(request: Request):
            try:
                return JSONResponse(self.connector.get_active_servers(True))
            except Exception as e:
                logger.error("Error fetch images, " + str(e))
                return None

    def start(self):
        uvicorn.run(self.app, host="0.0.0.0", port=8081)


if __name__ == "__main__":
    server = Server()
    server.start()