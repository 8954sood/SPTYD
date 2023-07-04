import re
from utiles.webbrowser.Chrome import Chrome
from typing import List, Union


class ChromeUsecase:
    
    @staticmethod
    async def openChrome(id:str, password:str, title:str, playlist: List[str]):
        chrome = Chrome(id, password)
        url = chrome.youtubeCreatePlaylist(title, playlist)
        url = f"https://www.youtube.com/playlist?list={ChromeUsecase.regexUrl(url)}"
        return url

    @staticmethod
    def regexUrl(url:str) -> str:
        playlist_id = re.search(r"/playlist/([^\s/]+)", url)
        if playlist_id:
            playlist_id = playlist_id.group(1)
        return playlist_id