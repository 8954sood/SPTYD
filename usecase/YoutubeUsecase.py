from utiles.api.AsyncYoutube import Youtube
from typing import Union, Dict

class YoutubeUsecase:
    
    @staticmethod
    async def getSearchTitle(title, api_key: str):
        youtube = Youtube(api_key)
        result =  await youtube.search_videos(title)
        # print(result)
        try:
            return result['items'][0]
        except:
            return False