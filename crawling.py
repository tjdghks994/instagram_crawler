from urllib.request import Request, urlopen, urlretrieve
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from multiprocessing import Pool, Value, freeze_support
import pandas as pd
import requests
import json
import os
import re


#게시글 url을 가져와서 리스트 형태로 return
def get_url_list() :
    url = "https://instagram.com/explore/tags/음식/"
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get(url)
    sleep(5)

    SCROLL_PAUSE_TIME = 1.0
    reallink = []

    while True :
        pageString = driver.page_source
        soup = BeautifulSoup(pageString, "lxml")

        for link in soup.find_all(name ="div", attrs={"class" : "Nnq7C weEfm"}) :
            for i in range(3) :
                title = link.select('a')[i]
                real = title.attrs['href']
                reallink.append(real)
            break
        break


        # last_height = driver.execute_script("return document.body.scrollHeight")
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # sleep(SCROLL_PAUSE_TIME)
        # new_height = driver.execute_script("return document.body.scrollHeight")

        # if new_height == last_height :
        #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #     sleep(SCROLL_PAUSE_TIME)
        #     new_height = driver.execute_script("return document.body.scrollHeight")

        #     if new_height == last_height :
        #         break
        #     else :
        #         last_height = new_height
        #         continue


    reallinknum = len(reallink)
    print(str(reallinknum)+"개의 게시물 URL 수집완료")
    reallink = list(set(reallink))
    driver.close()
    return reallink


#게시글로부터 음식사진, 해시태그, 시간 정보 가져오기
def get_info(url_list) :

    #쓸모없는 해시태그 list를 만들어서, 정규표현식으로 추후 해시태그 필터
    trash_list = ['반사', '팔', 'fff', 'f4f', 'follow', 'like', '일상', 
                'l4f', '좋반', '데일리', '셀카', '소통', '하면', '하자', '오오디디', 'oodd', '환영']

    csvtext = []
    driver = webdriver.Chrome('chromedriver.exe')
    

    for i in range(0, len(url_list)) :
        url = 'https://www.instagram.com/' + str(url_list[i])
        driver.get(url)
        csvtext.append([])

        pageString = driver.page_source
        soup = BeautifulSoup(pageString, "lxml")

        #게시글의 datetime 가져오기
        date = soup.select('time')[1]
        date = date.attrs['datetime']
        csvtext[i].append(date)

        #게시글의 hashtag 가져오기
        for hashtag in soup.find_all("meta", attrs={"property":"instapp:hashtags"}) :
            is_trash = False
            hashtag = hashtag['content']
            for trash in trash_list :
                if re.search(trash, hashtag) :
                    is_trash = True
                    break
            if not is_trash :
                csvtext[i].append(hashtag)

        #게시글의 imglink 가져오기
        while(1) :
            sleep(1)
            pageString = driver.page_source
            soup = BeautifulSoup(pageString, "lxml")
            imgs = soup.select('img')[1]
            imgs = imgs.attrs['src']
            csvtext[i].append(imgs)
            try :
                driver.find_element_by_class_name("coreSpriteRightChevron").click()
            except NoSuchElementException :
                break
    
    data = pd.DataFrame(csvtext)
    data.to_csv("insta.csv", encoding="utf-8-sig")
    print("저장완료")
    driver.close()
    
#list에 담겨있는 이미지 링크들을 다운로드하는 함수
def download_img(img_url_list) :
    for i in range(img_url_list) :
        urlretrieve(img_url_list[i], str(i) + ".jpg")

if __name__ == '__main__' :

    food_url_list = get_url_list()
    get_info(food_url_list)
    
