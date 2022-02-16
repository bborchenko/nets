import aiohttp
import asyncio
import logging
from traceback import format_exc


async def api_request(client, url):
    try:
        response = await client.get(url)
        response_dict = await response.json()
        return response_dict
    except Exception:
        logging.error(format_exc())


class App:
    def __init__(self, loop):
        super().__init__()
        self.loc = None
        self.coords = []
        self.i = 0
        self.loop = loop

    async def act(self):
        await self.get_location()
        tasks = []
        if self.loc:
            print('Choose: ')
            i = input()
            self.loc = self.coords[int(i) - 1]
            tasks.append(asyncio.create_task(self.get_weather()))
            tasks.append(asyncio.create_task(self.get_places()))
            await asyncio.gather(*tasks)

    async def get_location(self):
        print('Enter the location: ')
        location = input()
        key = 'c4a39929-cc5a-4959-958c-d26b2be94057'
        api_url = f'https://graphhopper.com/api/1/geocode?q={location}&locale=ru&debug=true&key={key}'

        async with aiohttp.ClientSession() as session:
            response_dict = await api_request(session, api_url)

            for hit in response_dict['hits']:
                address = hit['name'] + ', ' + hit['country'] + ', ' + hit['city']
                print(str(self.i + 1) + '. ' + address)
                self.loc = hit['point']
                coords = [hit['point']['lat'], hit['point']['lng']]
                self.coords.insert(self.i, coords)
                self.i = self.i + 1

    async def get_weather(self):
        lat = self.loc[0]
        lon = self.loc[1]
        api_key = 'b5a8070730e3c7716be730d471f9b32b'
        api_url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}'

        async with aiohttp.ClientSession() as session:
            response_dict = await api_request(session, api_url)

            weather = response_dict['weather'][0]['description']
            temperature = response_dict['main']
            print(weather, temperature)

    async def get_places(self):
        lat = self.loc[0]
        lon = self.loc[1]
        api_key = '5ae2e3f221c38a28845f05b649facbde0cb23865ae18af3fda5fb69a'
        api_url = f'http://api.opentripmap.com/0.1/ru/places/radius?radius=1000&limit=10&lon={lon}&lat={lat}&apikey={api_key}'

        async with aiohttp.ClientSession() as session:
            response_dict = await api_request(session, api_url)
            text = ''
            for place in response_dict['features']:
                properties = place['properties']
                if properties['name']:
                    text += str(properties['name']) + ', rate: ' + str(properties['rate']) + ', kinds: ' + str(properties['kinds']) + '\n'
                    await self.get_place_description(properties['xid'])

        print(text)

    async def get_place_description(self, xid):
        api_key = '5ae2e3f221c38a28845f05b649facbde0cb23865ae18af3fda5fb69a'
        api_url = f'http://api.opentripmap.com/0.1/ru/places/xid/{xid}?apikey={api_key}'
        async with aiohttp.ClientSession() as session:
            response_dict = await api_request(session, api_url)
            print(response_dict)
            return response_dict