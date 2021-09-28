from deriv_api.deriv_api_calls import DerivAPICalls
import websockets
import json
import logging

# TODO: remove after development
logging.basicConfig(
    format="%(asctime)s %(message)s",
    level=logging.DEBUG
)
class DerivAPI(DerivAPICalls):
    """Main class of the python DerivAPI module. It provides methods to connect, read and interact with API"""
    wsconnection:str = ''

    def __init__(self, app_id, endpoint = 'frontend.binaryws.com', lang = 'EN', brand = ''):
        connection_argument = {
            'app_id': str(app_id),
            'endpoint': endpoint,
            'lang': lang,
            'brand': brand
        }

        self.__set_apiURL(connection_argument)
        self.api_connect()

    def __set_apiURL(self, connection_argument):
        self.api_url = "wss://ws.binaryws.com/websockets/v3?app_id="+connection_argument['app_id']+"&l="+connection_argument['lang']+"&brand="+connection_argument['brand']

    def __get_apiURL(self):
        return self.api_url

    def api_connect(self):
        if not self.wsconnection:
            self.wsconnection = websockets.connect(self.api_url)
        return self.wsconnection

    async def send(self, message):
        return await self.send_receive(message)

    async def send_receive(self, message):
        async with websockets.connect(self.api_url) as websocket:
            await websocket.send(json.dumps(message))
            async for message in websocket:
                return self.parse_response(message)
   
    def parse_response(self, message):
        data = json.loads(message)
        return data