import re
from utiles.api.AsyncSpotify import AsyncSpotifySearch
from typing import Union, Dict


class SpotifyUsecase:
    
    @staticmethod
    async def getPlaylist(url) -> Union[bool, Dict[str, Dict[str, str]]]:
        client_id = "515d5213002a4776ab0668a3b988e119"
        client_secret = "27d42846d6364b6d93ad57d460fd496d"
        spotify = AsyncSpotifySearch(client_id, client_secret)
        await spotify.getToken()
        result = await spotify.track_search(url)
        
        return result