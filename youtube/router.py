from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, status
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import random
import time


def scroll(driver):
    try:        
        last_page_height = driver.execute_script("return document.documentElement.scrollHeight")
        while True:
            pause_time = random.uniform(1, 2)
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(pause_time)
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight-50)")
            time.sleep(pause_time)
            new_page_height = driver.execute_script("return document.documentElement.scrollHeight")
            
            if new_page_height == last_page_height:
                print("스크롤 완료")
                break
            else:
                last_page_height = new_page_height
    except Exception as e:
        print("에러 발생: ", e)

def scrape_youtube_results(keyword):
    service = Service(ChromeDriverManager(driver_version="111.0.5563.64").install())
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except ValueError as e:
        raise ValueError(f"웹드라이버 에러 발생! : {e}")

    SEARCH_KEYWORD = keyword.replace(' ', '+')
    URL = "https://www.youtube.com/results?search_query=" + SEARCH_KEYWORD
    driver.get(URL)
    # scroll(driver)
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ytd-video-renderer')))
    
    html_source = driver.page_source
    soup_source = BeautifulSoup(html_source, 'html.parser')
    content_total = soup_source.find_all(class_='yt-simple-endpoint style-scope ytd-video-renderer')
    content_total_title = list(map(lambda data: data.get_text().replace("\n", ""), content_total))
    content_total_link = list(map(lambda data: "https://youtube.com" + data["href"], content_total))

    # content_record_src = soup_source.find_all(class_='nline-metadata-item style-scope ytd-video-meta-block')
    # # content_record_src = soup_source.find_all(class_='shortViewCountText')
    # content_view_cnt = [content_record_src[i].get_text().replace('조회수 ', '') for i in range(5, len(content_record_src), 10)]
    # content_upload_date = [content_record_src[i].get_text() for i in range(6, len(content_record_src), 10)]
    # content_view_cnt = [content_record_src[i].get_text() for i in content_record_src]
    # content_upload_date = [content_record_src[i].get_text().replace('\n', '') for i in range(6, len(content_record_src), 10)]
    
    driver.quit()
    
    return {
        'title': content_total_title,
        'link': content_total_link,
        # 'view': content_view_cnt,
        # 'upload_date': content_upload_date
    }
youtube_video = APIRouter(prefix="/youtube", tags=["유튜브"])

@youtube_video.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="유튜브 스크래핑",
    description="좋아요 수, 조회수, 영상 링크, 영상 제목 스크래핑",
)
def get_video(keyword: str):
    results = scrape_youtube_results(keyword)
    return results