from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import pyautogui
import time
from typing import List, Union
import re

class Chrome:
    '''원래는 유튜브 api를 사용하여 해결하려했으나 Oauth2 문제로 실패'''
    def __init__(self, id: str, password: str) -> None:
        self.id = id
        self.password = password
    
    def writeText(self, driver, css:str, text:str) -> None:
        driver.find_element(By.CSS_SELECTOR, css).click()
        pyautogui.typewrite(text, interval=0.05)
    def waitBtnClick(self, driver, css:str) -> None:
        lBtn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, css))
        )
        lBtn.click()
    
    def google_login(self, driver) -> None:
        driver.get("https://accounts.google.com")

        #구글 로그인
        self.writeText(driver, 'input[type="email"]', self.id)
        next_button = driver.find_element(By.CSS_SELECTOR, '#identifierNext')
        next_button.click()
        driver.implicitly_wait(6)
        time.sleep(2.5)
        self.writeText(driver, 'input[type="password"]', self.password)

        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#passwordNext'))
        )
        login_button.click()
        time.sleep(2)
    
    def youtubeCreatePlaylist(self, title: int, playlist: List[str]) -> Union[bool, str]:
        '''숫자로 적힌 타이틀만 지원합니다.
        오류로 인해 리턴될시 False값이 반환됩니다.'''
        title = str(title)
        driver = uc.Chrome()
        self.google_login(driver)

        #재생목록 만들기
        driver.get("https://studio.youtube.com/channel/")
        self.waitBtnClick(driver, 'ytcp-button[id=create-icon]')
        time.sleep(1)
        self.waitBtnClick(driver, 'tp-yt-paper-item[id=text-item-2]')
        time.sleep(2)

        input_elements =  WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ytcp-social-suggestion-input[id=input]"))
        )
        input_elements[0].click()
        pyautogui.typewrite(title, interval=0.05)
        self.waitBtnClick(driver,  "ytcp-button[id=create-button]")
        time.sleep(4)
        #재생목록에 곡 추가
        for i in playlist:
            driver.get(i)
            driver.refresh() #해주지 않으면 ... 이 생성되지 않는 경우가 있다.

            time.sleep(1) #잠시 대기해야 오류 없음
            Container = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[id=actions]"))
            )
            Container.find_element(By.CSS_SELECTOR, "yt-button-shape[version=modern]").click()
            driver.implicitly_wait(6)
            Container = driver.find_elements(By.TAG_NAME, "ytd-menu-service-item-renderer")
            cnt = 1
            for i in Container:
                Name = i.find_element(By.TAG_NAME, 'yt-formatted-string')
                print(Name.text)
                if Name.text == "저장":
                    break
                cnt+=1
            #메뉴창 열기
            print(cnt)
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, f'//*[@id="items"]/ytd-menu-service-item-renderer[{cnt}]'))
            ).click()
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[id=playlists]"))
            ) #해당 태그가 생성된지 체크

            elements = driver.find_elements(By.TAG_NAME, 'ytd-playlist-add-to-option-renderer')
            cnt = 1
            # 요소들을 반복하여 작업 수행
            for element in elements:
                
                # yt-formatted-string 태그의 title 속성값 가져오기
                lTitle = element.find_element(By.TAG_NAME, 'yt-formatted-string').get_attribute('title')
                if lTitle == title:
                    break
                cnt +=1
            Container = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, f'//*[@id="playlists"]/ytd-playlist-add-to-option-renderer[{cnt}]'))
            ).click()
            
            time.sleep(1)
        #재생목록 url 구하기
        driver.get("https://studio.youtube.com/channel/content/playlists")
        time.sleep(1.5) #로딩 될때까지 잠시 대기

        Container = driver.find_elements(By.XPATH, f'//*[@id="playlist-title"]')
        for i in Container:  
            if i.text == title:
                url = driver.find_element(By.XPATH, f'//*[@id="row-container"]/div[1]/div/a').get_attribute("href")
                break
        driver.quit()
        return url
        
        




