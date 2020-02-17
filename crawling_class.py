from urllib.request import Request, urlopen, urlretrieve
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from time import time
from multiprocessing import Pool, Value, freeze_support
import pandas as pd
import requests
import json
import os
import re
from selenium.webdriver.chrome.options import Options
import numpy as np
import platform

class instagram_crawler :

    def __init__(self) :
        self.url = None
        self.collected_url = None
        self.data = None
        self.options = None
        self.path = None
    
    def set_path(self, path) :
        self.path = path
    def set_url(self, url) :
        self.url = url
    
    def set_options(self) :
        self.options = Options() 
        prefs = {'profile.default_content_setting_values': {'images': 2, #'cookies' : 2,
                                                            'plugins' : 2, 'popups': 2, 
                                                            'geolocation': 2, 'notifications' : 2, 
                                                            'auto_select_certificate': 2, 'fullscreen' : 2, 
                                                            'mouselock' : 2, 'mixed_script': 2, 
                                                            'media_stream' : 2, 'media_stream_mic' : 2, 
                                                            'media_stream_camera': 2, 'protocol_handlers' : 2, 
                                                            'ppapi_broker' : 2, 'automatic_downloads': 2, 
                                                            'midi_sysex' : 2, 'push_messaging' : 2, 
                                                            'ssl_cert_decisions': 2, 'metro_switch_to_desktop' : 2, 
                                                            'protected_media_identifier': 2, 'app_banner': 2, 
                                                            'site_engagement' : 2, 'durable_storage' : 2}} 
        self.options.add_experimental_option('prefs', prefs) 
        self.options.add_argument("start-maximized") 
        self.options.add_argument("disable-infobars") 
        self.options.add_argument("--disable-extensions") 
        
        #창 없는 크롬으로 실행하는 옵션
        self.options.add_argument('--headless')    
    

    #게시글 url을 수집
    def collect_url(self, count) :
        url = self.url
        
        print('현재 OS = ' + platform.system())

        if (platform.system() == "Windows") :
            driver = webdriver.Chrome(self.path + 'chromedriver.exe',options = self.options)
        else :
            driver = webdriver.Chrome(self.path + 'chromedriver',options = self.options)
        
        
        driver.get("https://www.instagram.com/accounts/login/?source=auth_switcher")
        driver.implicitly_wait(1)
        driver.find_elements_by_name("username")[0].send_keys("goka2052")
        driver.find_elements_by_name("password")[0].send_keys("dlstmxk2052")
        elem = driver.find_elements_by_name("password")[0]
        elem.send_keys(Keys.RETURN)
        sleep(3)

        driver.get(url)
        driver.implicitly_wait(1)
        SCROLL_PAUSE_TIME = 3
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

        reallink = list(set(reallink))
        print(str(len(reallink))+"개의 게시물 URL을 수집했습니다.")

        driver.close()
        self.collected_url = reallink



    #게시글로부터 음식사진, 해시태그, 시간 정보 가져와 dataframe으로 만들기
    def make_data(self) :

        #쓸모없는 해시태그 list를 만들어서, 정규표현식으로 추후 해시태그 필터
        trash_list = ['반사', '팔', 'fff', 'f4f', 'follow', 'like', '일상', '스타', '그램', 'lfl', '좋튀', '댓글', '음식',
                    'l4f', '좋반', '데일리', '셀카', '소통', '하면', '하자', '오오디디', 'oodd', '환영']
        csvtext = []
        

        if (platform.system() == "Windows") :
            driver = webdriver.Chrome(self.path + 'chromedriver.exe',options = self.options)
        else :
            driver = webdriver.Chrome(self.path + 'chromedriver',options = self.options)
        

        error = 0

        for i in range(0, len(self.collected_url)) :
            if i%20 == 0 :
                print('진행상황: ' + str(i))
            try :
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

            except Exception as e :
                print('make data 예외 발생', e)
                error += 1
                for j in range(6) :
                    csvtext[i].append("0")

        
        print('make data 예외 발생 횟수 = %d' % error)

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
        self.create_folder()

        filenum = 1
        for i in img_url_list :
            for j in i :
                try :
                    if j == '0' or j == 0 :
                        continue
                    r = requests.get(j)
                    with open(self.path + 'img_crawl/' + str(filenum) + '.jpg', 'wb') as outfile:
                        outfile.write(r.content)

                except Exception as e :
                    print('download img 예외 발생', e)

                filenum += 1

    def create_folder(self) :
        try :
            if not os.path.exists(self.path + 'img_crawl') :
                os.makedirs(self.path + 'img_crawl')
        except OSError :
            print('create folder 예외발생', OSError)



if __name__ == '__main__' :

    start_time = time()


    crawler = instagram_crawler()
    crawler.set_options()

    if (platform.system() == "Windows") :
        path = ''
    else :
        path = '/Users/psh/Python/instagram_crawler/'

    crawler.set_path(path)

    keyword = input("크롤링할 해쉬태그를 입력하세요 ")
    url = "https://instagram.com/explore/tags/" + str(keyword)
    crawler.set_url(url)

    count = int(input("최대 게시글 갯수를 입력해주세요 "))

    crawler.collect_url(count)


    crawler.make_data()
    crawler.save_data("insta_test.csv")


    data = pd.read_csv("insta_test.csv")
    img_url_list = data[['4','5','6']]
    img_url_list = img_url_list.values.tolist()    
    crawler.download_img(img_url_list)

    print("%s초 걸림" % (time() - start_time))

