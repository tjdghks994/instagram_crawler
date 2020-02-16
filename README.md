# Instagram_crawler

인스타 크롤러 만들기

  - **CAU CPS LAB** - 박성환
  - **학부 연구생** - 최병준, 임채원

# Install Package

```
pip install beautifulsoup4
pip insatll pandas
pip install requests
pip install selenium
pip install lxml
```

# AS-IS

## ~20.02.17

- 크롤링 속도 개선
  - 병준 : Chrome Driver에 Options을 주고 sleep 시간 최소화시킴 (완료 / 20.02.12)
    - 약 1/3 단축
    - 참고
      - https://beomi.github.io/gb-crawling/posts/2017-09-28-HowToMakeWebCrawler-Headless-Chrome.html
      - https://pcmc.tistory.com/66
  
  - 병준 : try / except로 코드 변경하여 예외처리 해주기 (완료 / 20.02.12)
  
  - 인스타 자동 로그인
    - 로그인이 되어있지 않으면 게시물을 계속해서 가져올 수 없음
    - 병준 : 자동 로그인 구현하기 (완료 / 20.02.12)
    - 참고
      - https://enfanthoon.tistory.com/87
- 음식/비음식 식별 YOLO
  - 채원 : PyTorch-YOLOv3 에서 darknet yolo로 변경(2/10, 그 전까지는 계속 이전에 사용한 코드 수정하고 다시 짜고 하다가 포기), face 클래스 하나만으로 112개 데이터세트를 갖고 했을 때는 test했을 때 사람이 나온 사진에서 얼굴 검출 성공(2/11) --> face, dog, cat, desk, chair 5가지 클래스, 각각 50, 48, 48, 16, 69개 데이터세트를 가지고 학습을 시험삼아 시켜 봤지만(학습 당 9초-->5초-->4초 가량 소요) 285번째에서 평균 loss 1.370703이 최대, colab에서 돌릴 시에 계속 런타임 오류 혹은 아예 크롬이 꺼짐(가중치 파일도 저장되지 않으면서 꺼짐 --> detector 파일 수정, 100 단위에서 가중치 파일 저장) --> 적어도 클래스 당 100개 이상의 사진을 가지고 학습을 시켜봐야하는데 현재는 colab에서 할 시 계속 오류가 나는 상태(2/14~16) --> 학교 컴퓨터로 가상환경에서 재학습 필요
- 색 검출 알고리즘
  - 채원 : K-Nearest Neighbors 기반, https://github.com/ahmetozlu/color_recognition 참고

## ~20.01.31

  - 음식사진 + 해시태그 + 시간 같이 긁어오기
      - 병준 : [datetime, hashtags, imglinks] 형태로 csv에 저장 (완료 / 20.01.20)
          - hashtag 개수와 img 개수에 따라 열 갯수가 달라지는데, 이를 어떻게 해결해야 할지 생각해보기
            - 최대 3개씩으로 설정했음. 만약, 3개 이하로 존재하는 경우 0으로 채워넣음 (완료 / 20.01.28)
  - 크롤링 코드 커밋하기
      - 병준 : 커밋함 (완료 / 20.01.20)
  - 코드 모듈화 하여 추후에도 사용 가능하게 만들기
      - 병준 : 코드 모듈화 시키기 (완료(수정 완료) / 20.01.25(20.01.28))

# TO-BE

  - 2016년 ~ 2019년 ,1월 ~ 12월, 우리나라 비만율, 홍콩 비만율 비교 (평균 비만율로 하면 됨 / 나이대 무시)
    - 채원 & 병준 : 추후 조사하기
  
  - 음식 색 구분
    - 채원&병준 : 색 검출 알고리즘 찾아보기
    - https://github.com/beerboaa/Color-Classification-CNN 참고하기
    - **k-means clustering** 조사하기
      - 색 구분 알고리즘
  
  - Multi-processing  
    - 병준 : multiprocessing 적용하기
    - 적용하기가 생각보다 쉽지 않아서 고민

  - Crewling
    - tag가 음식 하나만 하기에는 너무 부실함, 맛집 등 새로운 태그 추가

  - README.md update
    - Python 및 각 모듈 버전 명시
    - Reference 추가해두기
    - 'chromedrive -> chrome 버전 80 이상에서만 사용가능' 추가
  
  - 가능하다면 macos 대응해주기
