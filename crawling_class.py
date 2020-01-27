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

class instagram_crawler :

    def __init__(self) :
        self.url = None
        self.collected_url = None
        self.data = None

    def set_url(self, url) :
        self.url = url

    #게시글 url을 수집
    def collect_url(self, count) :
        url = self.url
        driver = webdriver.Chrome('chromedriver.exe')
        driver.get(url)
        sleep(5)
        SCROLL_PAUSE_TIME = 1.0
        reallink = []
        finish = False

        while True :
            pageString = driver.page_source
            soup = BeautifulSoup(pageString, "lxml")

            for link in soup.find_all(name ="div", attrs={"class" : "Nnq7C weEfm"}) :
                for i in range(3) :
                    title = link.select('a')[i]
                    real = title.attrs['href']
                    reallink.append(real)
                
                count = count - 3
                if(count <= 0) :
                    finish = True
                    break
            
            if(finish == True) :
                break

            last_height = driver.execute_script("return document.body.scrollHeight")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height :
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(SCROLL_PAUSE_TIME)
                new_height = driver.execute_script("return document.body.scrollHeight")

                if new_height == last_height :
                    break
                else :
                    last_height = new_height
                    continue


        reallinknum = len(reallink)
        print(str(reallinknum)+"개의 게시물 URL 수집완료")
        reallink = list(set(reallink))
        driver.close()
        self.collected_url = reallink

    #게시글로부터 음식사진, 해시태그, 시간 정보 가져와 dataframe으로 만들기
    def make_data(self) :

        #쓸모없는 해시태그 list를 만들어서, 정규표현식으로 추후 해시태그 필터
        trash_list = ['반사', '팔', 'fff', 'f4f', 'follow', 'like', '일상', '스타', '그램', 'lfl', '좋튀', '댓글', '음식',
                    'l4f', '좋반', '데일리', '셀카', '소통', '하면', '하자', '오오디디', 'oodd', '환영']
        csvtext = []
        driver = webdriver.Chrome('chromedriver.exe')
        
        for i in range(0, len(self.collected_url)) :
            url = 'https://www.instagram.com/' + str(self.collected_url[i])
            driver.get(url)
            csvtext.append([])

            pageString = driver.page_source
            soup = BeautifulSoup(pageString, "lxml")

            #게시글의 datetime 가져오기
            date = soup.select('time')[1]
            date = date.attrs['datetime']
            csvtext[i].append(date)
            max_cnt = 0

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
                    max_cnt += 1

                if max_cnt >= 3 :
                    break
            while(max_cnt < 3) :
                csvtext[i].append("0")
                max_cnt += 1

            #게시글의 imglink 가져오기
            max_cnt = 0
            while(1) :
                sleep(1)
                pageString = driver.page_source
                soup = BeautifulSoup(pageString, "lxml")
                imgs = soup.select('img')[1]
                imgs = imgs.attrs['src']
                csvtext[i].append(imgs)
                max_cnt += 1

                if max_cnt >= 3 :
                    break
                try :
                    driver.find_element_by_class_name("coreSpriteRightChevron").click()
                except NoSuchElementException :
                    break

            while(max_cnt < 3) :
                csvtext[i].append("0")
                max_cnt += 1

        self.data = pd.DataFrame(csvtext)
        driver.close()

    def get_collected_url(self) :
        return self.collected_url

    def get_data(self) :
        return self.data

    def save_data(self, filename) :
        self.data.to_csv(filename, encoding="utf-8-sig")
        print("저장완료")

    #list에 담겨있는 이미지 링크들을 다운로드하는 함수
    def download_img(self, img_url_list) :
        for i in range(img_url_list) :
            urlretrieve(img_url_list[i], str(i) + ".jpg")


if __name__ == '__main__' :

    crawler = instagram_crawler()

    keyword = input("크롤링할 해쉬태그를 입력하세요 ")
    url = "https://instagram.com/explore/tags/" + str(keyword)
    crawler.set_url(url)

    count = int(input("게시글 갯수를 입력하세요 "))

    crawler.collect_url(count)
    crawler.make_data()
    crawler.save_data("insta_test.csv")