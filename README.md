# 프로젝트 개요

AWS EC2, RDS와 머신러닝 기반 추천 기능을 활용한 와인 검색, 판매 및 구매 서비스 Wining입니다.

국내 와인 소비량은 해마다 증가중에 있으나 와인을 잘 선택해서 즐기기에는 입문 장벽이 너무 높다는 점을 어려움으로 꼽을 수 있습니다. 이에 사용자의 취향을 기반으로 와인을 선택할 수 있게 해주는 서비스를 구상하게 되었습니다.

# 프로젝트 진행 기간
- 2023.06.05~2023.09.04(풀 스택 4명)


# 프로젝트 실행 화면
- 일반 회원 정보 페이지
![mypage](https://github.com/HTH016/Wining/assets/129934364/07ab4afa-8857-438d-ab71-68eede0e7bd5)

- 자유 게시판
![board](https://github.com/HTH016/Wining/assets/129934364/25b61e0a-28a5-4840-890d-c5bbb2ceb2c9)
![boaard2](https://github.com/HTH016/Wining/assets/129934364/030ec7bf-a525-4c34-8613-a232c8d367fa)

- 점포 정보 페이지
![storeinfo](https://github.com/HTH016/Wining/assets/129934364/4aa33173-3f6b-4c12-ac5a-400ddf28f2ec)

- 결제 페이지
![paying](https://github.com/HTH016/Wining/assets/129934364/d3fce7fe-a49f-49c7-912a-18882e574a1e)



# 사용 기술
- Front-end
  - Vue.js 3.3.4
  - JQuery 3.6.4
  - Bootstrap 5.3.0 / 5.0.0
- Back-end
  - Python 3.8
  - Django 4.2.2
  - Django Rest Framework 3.14.0
  - MySQL 8.0.33
- 기타
  - Git
  - gunicorn 20.1.0
  - Nginx 1.24
  - Docker 24.0.5
  - Docker Compose 2.20
  - AWS(Amazon Web Service) EC2, RDS
- BigData
  - Pandas 2.0.2
  - Scikit-learn 1.1.2
  - Numpy 1.24.3
# 실행환경 및 실행 방법

- AWS ~~<http://sample-elb-1600299374.ap-northeast-2.elb.amazonaws.com/search/main>~~ 현재 접속 불가
- python 3.8, MySQL 8.0.33 필요
  - Window (Window 10 권장)
  
    
    <https://github.com/HTH016/Wining/releases/tag/published> 에서 소스코드 다운
  
    임의의 경로에 압축 해제
  
    명령프롬포트 실행 후 압축 해제한 경로로 이동
  
    mysql 접속
  
    ```
    create database bit;
    ```
    mysql 로그아웃
    ```
    mysql -u계정이름 -p bit < 소스코드 루트 경로\bit_save.sql
    ```
  
    ```
    pip install -r window_requirements.txt
    ```
  
    ```
    python dev_manage.py runserver
    ```
  
    
  - Linux(가상머신)
  
    - Ubuntu 20.04 LTS 권장, Git, Docker 24.0.5, Docker Compose 2.20.2 설치 필요
    ```
    mkdir wining
    ```
    
    ```
    cd wining
    ```
    
    ```
    git clone https://github.com/HTH016/Wining.git
    ```
    
    ```
    cd Wining
    ```
    
    ```
    git checkout product
    ```
    
    ```
    sudo docker compose up --build
    ```

- 서비스 접속

  - 기본 페이지 접속 <http://가상머신의ip/search/main> / <http://127.0.0.1:8000/search/main>
  - 일반 유저의 경우 기본 페이지 접속 후 Login - Regist with Kakao 클릭 - 회원가입 진행 후 myPage
  - 점주 유저의 경우 기본 페이지 접속 후 Login - Regist with Kakao 클릭 - store 클릭 - 회원가입 진행 후 myPage - 점주페이지
  - 관리자 접속 <http://가상머신의ip/admin> / <http://127.0.0.1:8000/admin> ID: admin / PW: admin1234

# 역할 분담
- HTH016
  - 조장
  - 데이터베이스 설계
  - 와인 검색 (search) front-end 및 back-end 구현
  - 와인 상세 정보 (detail) front-end 및 back-end 구현
  - 와인 추천 모듈(recommendModules) 설계 및 구현

- HoomanHoo
  - 담당 업무 -  Front-End, Back-End, 배포
  - Front-End
    - Intersection Observer API와 Vue.js를 이용한 무한 스크롤 기능으로 매장 리스트 살펴보기 기능 구현
    - Fetch API와 Vue.js를 활용하여 상품 댓글 정렬, 포인트 충전 및 결제 수단 등록, 연관 검색어 표시 기능 구현
    - 페이징 처리와 Fetch API, ajax를 이용하여 판매할 와인 선택, 와인 이름으로 검색, 매출 정보 확인 기능 구현
    - Fetch API를 이용하여 수령 코드 검색, 수령 확인 기능 구현
    - 다음 주소 찾기 API와 Javascript 정규식을 이용하여 입력한 점포 정보 입력 기능 구현

  - Back-End
    - 고객, 점주를 기준으로 기능 분석을 진행한 뒤 DB 설계에 참여
    - 비동기 함수를 이용하여 구매 목록, 주문 목록 메일 발송 소요 시간 최소화
    - Django ORM을 통한 DB Access 코드 구현 효율화 (if문 분기에 따른 매개변수 변경으로 상황에 따라 다른 DB Query가 실행될 수 있도록 구현)
    - django rest framework를 이용하여 ajax, FetchAPI 통신 시 세분화된 HTTP Request를 처리할 수 있도록 구현, Serializer를 통한 JSON 포맷 컨버팅 구현
    - Kakao Login API를 이용해 받아온 연령대 정보로 회원 가입 연령대 제한
    - 점포 정보 등록, 수정, 삭제에 대한 CRUD 기능 구현
    - 판매 상품 등록, 수정 기능 구현 
    - 장바구니 상품 등록, 삭제 기능 구현
    - 포인트 결제 및 상품 구매 기능 구현
    

  - 기타 사항
    - 개발 환경과 실행 환경 설정 분리(manage.py와 settings.py, wsgi.py를 개발용(Windows용)과 실행용(Linux용) 으로 나눔)
    - Git (Tortoise Git, Github Desktop, Git CLI)을 통한 코드 버전 관리
    - Nginx 연동으로 static file serving에 대한 WAS의 부담 경감
    - Docker Compose를 이용하여 개발, 배포환경을 동일하게 유지, Host OS 변경에 따른 오작동 요소 최소화
    - AWS 배포 시 2개의 EC2 Instance, Elastic LoadBalancer, RDS를 사용하여 트래픽 분산 처리 설정

- nzxxxx
  - 일반 사용자 정보 관리(user) front-end 및 back-end 구현
  - 와인 추천 모듈(recommendModules) 내장 함수 구현

- Minseo-0619
  - 게시판(board) front-end 및 back-end 구현
  -  웹UI/UX 설계 및 적용



# 시스템 구성도

![wining 발표 책자 수정본](https://github.com/HoomanHoo/WiningFull/assets/129934364/6a0655df-2562-4f85-bde0-28797772bd4c)


# ERD 설계

![erd](https://github.com/HoomanHoo/WiningFull/assets/129934364/667b9326-2715-45fc-9ede-1aabe74d9df0)
