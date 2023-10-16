# 프로젝트 개요

AWS EC2, RDS와 머신러닝 기반 추천 기능을 활용한 와인 검색, 판매 및 구매 서비스 Wining입니다.
국내 와인 소비량은 해마다 증가중에 있으나 와인을 잘 선택해서 즐기기에는 입문 장벽이 너무 높다는 점을 어려움으로 꼽을 수 있습니다. 이에 사용자의 취향을 기반으로 와인을 선택할 수 있게 해주는 서비스를 구상하게 되었습니다.

# 역할 분담
- HTH016
  - 조장
  - 데이터베이스 설계
  - 와인 검색 (search) front-end 및 back-end 구현
  - 와인 상세 정보 (detail) front-end 및 back-end 구현
  - 와인 추천 모듈(recommendModules) 설계 및 구현

- HoomanHoo
   - 데이터베이스 설계
   - 와인 구매(purchasing) front-end 및 back-end 구현
   - 점포 정보 관리(store) front-end 및 back-end 구현
   - 일반 사용자 정보 관리(user) 모듈 내 Kakao Login API를 이용한 SNS 계정을 사용한 회원가입 및 로그인 기능, 포인트 충전 및 결제수단 등록, 관리 기능 front-end 및 back-end 구현
   - Docker, Docker Compose 환경 설정
   - AWS 배포 환경 설정

- nzxxxx
  - 일반 사용자 정보 관리(user) front-end 및 back-end 구현
  - 와인 추천 모듈(recommendModules) 내장 함수 구현

- Minseo-0619
  - 게시판(board) front-end 및 back-end 구현
  -  웹UI/UX 설계 및 적용

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




# 시스템 구성도

![wining 발표 책자 수정본](https://github.com/HoomanHoo/WiningFull/assets/129934364/6a0655df-2562-4f85-bde0-28797772bd4c)


# ERD 설계

![erd](https://github.com/HoomanHoo/WiningFull/assets/129934364/667b9326-2715-45fc-9ede-1aabe74d9df0)
