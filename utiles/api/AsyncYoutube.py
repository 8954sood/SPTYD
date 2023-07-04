from typing import Union
import aiohttp
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account

class Youtube:
    def __init__(self, api_key: str) -> None:
        # self.api_key = "AIzaSyA1NAlUF8FWzymVEugBRFTY8bx2YQuUrAM"
        self.api_key = api_key
        # self.api_key = "AIzaSyB3ypNfD7ZF-Xb63ppbS0Myjuxwf5n3XCk"

    async def search_videos(self, query: str):
        async with aiohttp.ClientSession() as session:
            try:
                response = await session.get(
                    'https://www.googleapis.com/youtube/v3/search',
                    params={
                        'part': 'snippet',
                        'q': query,
                        'type': 'video',
                        'maxResults': 1,
                        'key': self.api_key
                    }
                )
                data = await response.json()
                return data
            except aiohttp.ClientError as e:
                # print('An error occurred:', e)
                return False
