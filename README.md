# Instagram_crawler

인스타 크롤러 만들기

  - cau cps lab - 박성환
  - 학부 연구생 - 최병준, 임채원

# Install Package

```
pip install beautifulsoup4
pip insatll pandas
pip install requests
pip install selenium
pip install lxml
```

# TODO

  - 음식사진 + 해시태그 + 시간 같이 긁어오기
      - 병준 : [datetime, hashtags, imglinks] 형태로 csv에 저장 (완료 / 20.01.20)
          - hashtag 개수와 img 개수에 따라 열 갯수가 달라지는데, 이를 어떻게 해결해야 할지 생각해보기
            - 최대 3개씩으로 설정했음. 만약, 3개 이하로 존재하는 경우 0으로 채워넣음 (완료 / 20.01.28)
  - 크롤링 코드 커밋하기
      - 병준 : 커밋함 (완료 / 20.01.20)
  - 코드 모듈화 하여 추후에도 사용 가능하게 만들기
      - 병준 : 코드 모듈화 시키기 (완료(수정 완료) / 20.01.25(20.01.28))
      - ~~채원 : 모듈화된 것 문서화 시키기~~
  - 음식을 종류별로 나누기 : 초록색은 풀, 노랑색은 기름진거
    - 채원&병준 : 색 검출 알고리즘 찾아보기
    https://github.com/beerboaa/Color-Classification-CNN 참고할 
  - 음식인지 아닌지
      - 채원 : YOLO 이용하기 - yolo v3(https://github.com/eriklindernoren/PyTorch-YOLOv3) 사용, train/detect/config/data 등 맞춰서 수정
        - colab에서 train 돌릴 때 data configuration 부분에서 오류 계속 발생(path 문제인 듯 함)
       - training dataset 설정 : #음식, #맛집으로 검색하면 얼굴, 식당 내부 풍경, 멍멍이, 고양이 등 다양한 사진이 같이 나옴
       이거 정제하기 위해서 yolo를 사용해 face(face, half_face, phone_face), chair, desk, dog, cat 의 점수가 높게 나온 사진들은 제외 
       인스타그램 크롤러(병준이가 만든거) 사용해서 #얼굴, #댕스타그램, #반려묘, #카페의자추천, #카페식탁 / 100개 게시글 크롤링해서 이미지   
       추출 후 labeimg 사용해서 이미지 라벨링 완료 -> plate 폴더에 저장 
  - 인스타그램 크롤링 되는지 안되는지
      - 잘 모르겠음...
  - 2016년 ~ 2019년 ,1월 ~ 12월, 우리나라 비만율, 홍콩 비만율 비교 (평균 비만율로 하면 됨 / 나이대 무시)
      - 채원 & 병준 : 추후 조사하기
  - 속도가 느리면 go, c++ 이용
        - 다 만든 후에 적용
  - 어떤 데이터가 유의미한 데이터일지 판단하기
  - 아이디어 서로 내보기

