import json
from pathlib import Path
import asyncio
from reactpy import component, hooks, html, run, use_state, event
from utiles.Link import is_spotify_playlist_link
import webbrowser
from usecase.ChromeUsecase import ChromeUsecase
from usecase.SpotifyUsecase import SpotifyUsecase
from usecase.YoutubeUsecase import YoutubeUsecase
import json

with open("./config.json", "r", encoding="utf-8") as E:
    config = json.loads(E.read())
id = config['id']
password = config['password']
api_key = config['api_key']
li_style = {"style": {"font-size": "20px", "margin-top": "5px"}}
count = 0
searchIt = False

def logAdd(text: str) -> html.li:
    return html.li(li_style, text)
@component
def SPTYD():
    message, set_message = use_state("")
    logLs, logSet = use_state([html.h1(li_style, "무조건 키보드 언어설정을 '영어'로 해주세요")])
    
    @event(prevent_default=True)
    async def handle_click(event):
        logSet([])
        global searchIt
        global count
        if searchIt:
            return print("검색중임")
        logList = []
        if not is_spotify_playlist_link(message):
            return set_message("올바르지 않은 플레이리스트 링크입니다.")
        set_message("플레이 리스트를 생성중입니다.")
        urls = str(message)
        searchIt = True
        
        result = await SpotifyUsecase.getPlaylist(message)
        if result is False:
            logList.append(logAdd("올바르지 않은 플레이리스트 링크입니다."))
            return logSet(logList)
        logList.append(logAdd("플레이 리스트 링크 검사 성공"))
        
        playlist = []
        for i in result.keys():
            logList.append(logAdd(".."))
            i = result[i]
        
            youtube_search = (await YoutubeUsecase.getSearchTitle(f"{i['title']} - {i['artist']}", api_key))
            if youtube_search is False:
                logList.append(logAdd("API 한도 초과로 리퀘스트에 실패하였습니다."))
                logSet(logList)
                searchIt = True
                return
            print(youtube_search)
            url = "https://www.youtube.com/watch?v=" + youtube_search['id']['videoId'] 
            playlist.append(url)
            logList.append(logAdd(f"url 추가 : {url}"))
        '''플리 생성'''
        logList.append(logAdd("재생목록 생성 중"))
        
        await asyncio.sleep(0.2)
        count +=1 
        try:
            chrome = await ChromeUsecase.openChrome(id, password, count, playlist) 
        except:
            logList.append(logAdd(f"알 수 없는 이유로 실패하였습니다. 재시도 부탁드립니다."))
            logSet(logList)
            set_message("생성에 실패하였습니다. 아래 로그를 확인해주세요.")
            searchIt = False
            return
        #비동기로 처리하지 않는 이유 : selenium만 사용하면 비동기로 처리가 가능하지만
        #구글 로그인 상의 문제로 pyautogui를 사용해야 하기떄문에 동기로 처리하여 순서대로 처리
        logList.append(logAdd(f"재생목록 생성 성공! : {chrome}"))
        logSet(logList)
        
        set_message("생성이 완료되었습니다. 아래 로그를 확인해주세요")
        searchIt = False
        
        return html.h1("ㄱㄱ")
    logo = "https://github.com/8954sood/SPTYD/blob/main/logo.png?raw=true"
    # return html.template("htmltest.html")
    return html.div({"style": {
        "box-sizing": "border-box",
        "display": "flex",
        "flex-direction": "column",
        "align-items": "center",
        "padding": "10px",
        "gap": "10px",
        "position": "relative",
        "width": "1440px",
        "height": "1024px",
        "background": "#FFFFFF"
        
    }},
        html.img({'src': logo, "style": {
            "width": "568px",
            "height": "352px"
        }}),
        html.div({"style": {
            "box-sizing": "border-box",
            "position": "absolute",
            "left": "15.28%",
            "right": "15.28%",
            "top": "36.33%",
            "bottom": "44.14%",
            "background": "#FFFFFF",
            "border": "1px solid #000000",
            "border-radius": "20px"
            }},
            html.input({
                "type": "text",
                "placeholder": "스포티파이 플레이 리스트 링크를 입력하세요.",
                "value": message,
                "on_change": lambda event: set_message(event["target"]["value"]),
                "style": {
                "position": "absolute", 
                "left": "1.46%",
                "right": "36.67%",
                "top": "20%",
                "bottom": "48.54%",
                "background": "#1DB954",
                "border-radius": "10px",
                "width": "675px",
                "height": "111px",
                "color": "#FFFFFF",
                "font-size": "20px"
            }}),
            html.button({"on_click": handle_click, "style": {
                "position": "absolute",
                "width": "271px",
                "height": "111px",
                "left": "71.46%",
                "right": "36.67%",
                "top": "20%",
                "bottom": "48.54%",
                "color": "#FFFFFF",
                "font-size": "25px",
                "background": "#1DB954",
                "box-shadow": "0px 4px 4px rgba(0, 0, 0, 0.25)",
                "border-radius": "30px"
                }}, "Search"),
            
            
        ),
        html.div({"style": 
                 {
                    "position": "absolute",
                    "left": "15.28%",
                    "right": "15.28%",
                    "bottom": "44.14%",
                    "top":"70%",
                    "height": "200px",
                    "overflow-y": "scroll",
                    "border": "1px solid #000000",
                    "border-radius": "20px"
                }
                }, 
                html.ul({"style": {
                    "list-style-type": "none"}},
                    logLs
            )
        )

    )
webbrowser.open("http://localhost:8001")
run(SPTYD, "0.0.0.0", "8001")
