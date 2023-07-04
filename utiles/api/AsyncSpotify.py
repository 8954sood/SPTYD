import re
from typing import Optional, Union
import aiohttp
import base64
from utiles.error.Error import *


class AsyncSpotifySearch:
    def __init__(self, client_id: str, client_secret: str):
        self.prefix = "https://api.spotify.com/v1/"
        self.language = "KR"
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None

    async def getToken(self):
        try:
            auth_str = f"{self.client_id}:{self.client_secret}"
            auth_b64 = base64.b64encode(auth_str.encode()).decode()

            auth_url = "https://accounts.spotify.com/api/token"
            auth_headers = {
                "Authorization": f"Basic {auth_b64}"
            }
            auth_data = {
                "grant_type": "client_credentials"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(auth_url, headers=auth_headers, data=auth_data) as response:
                    data = await response.json()
                    self.token = data["access_token"]
        except:
            raise failedGetToken

    async def track_search(self, url: str) -> Union[dict, bool]:
        if self.token is None:
            raise invalidToken
        playlist_id = re.search(r'playlist/([a-zA-Z0-9]+)', url)
        if playlist_id:
            url = playlist_id.group(1)
        else:
            raise invaildSearchUrl
        try:
            get_url = f"https://api.spotify.com/v1/playlists/{url}"
            get_headers = {
                'Authorization': f'Bearer {self.token}',
                'market': self.language
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(get_url, headers=get_headers) as response:
                    data = await response.json()
                    result = {}
                    for item in data['tracks']['items']:
                        track = item['track']
                        result[track['name']] = {'title': track['name'],
                                                 'artist': track['artists'][0]['name']}
                        
                    return result

        except:
            return False