class Server():
    id:str
    latitude:int
    longitude:int
    location:str
    provider:str
    country:str
    status:str

    def __init__(self,id,latitude,longitude,location,provider,country,status=1):
        self.id=id
        self.latitude=latitude
        self.longitude = longitude
        self.location = location
        self.provider=provider
        self.country = country
        self.status = status

    def __eq__(self, other):
        if isinstance(other, Server):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)
