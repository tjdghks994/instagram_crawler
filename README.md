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

## ~20.02.17

- 크롤링 속도 개선
  - 병준 : Chrome Driver에 Options을 주고 sleep 시간 최소화시킴 (완료 / 20.02.12)
    - 약 1/3 단축
  - 병준 : try / except로 코드 변경하여 예외처리 해주기 (완료 / 20.02.12)
  
  - 인스타 자동 로그인
  - 로그인이 되어있지 않으면 게시물을 계속해서 가져올 수 없음
    - 병준 : 자동 로그인 구현하기 (완료 / 20.02.12)
  - 병준 : multiprocessing 적용하기
    - 적용하기가 생각보다 쉽지 않아서 고민
  
- 음식 색 구분
  - 채원&병준 : 색 검출 알고리즘 찾아보기
  - https://github.com/beerboaa/Color-Classification-CNN 참고하기
  
- 2016년 ~ 2019년 ,1월 ~ 12월, 우리나라 비만율, 홍콩 비만율 비교 (평균 비만율로 하면 됨 / 나이대 무시)
  
  - 채원 & 병준 : 추후 조사하기

## ~20.01.31

  - 음식사진 + 해시태그 + 시간 같이 긁어오기
      - 병준 : [datetime, hashtags, imglinks] 형태로 csv에 저장 (완료 / 20.01.20)
          - hashtag 개수와 img 개수에 따라 열 갯수가 달라지는데, 이를 어떻게 해결해야 할지 생각해보기
            - 최대 3개씩으로 설정했음. 만약, 3개 이하로 존재하는 경우 0으로 채워넣음 (완료 / 20.01.28)
  - 크롤링 코드 커밋하기
      - 병준 : 커밋함 (완료 / 20.01.20)
  - 코드 모듈화 하여 추후에도 사용 가능하게 만들기
      - 병준 : 코드 모듈화 시키기 (완료(수정 완료) / 20.01.25(20.01.28))

