## Description
- 더존에 알맞는 엑셀 변환기 (휴먼스케이프)
- 카드사 결제 내역 (+ 인명부 + 슬랙 채널 댓글 모음) => 더존용으로 포맷 변환
- 회계팀 수작업을 줄이려는 앱
- 댓글 검색범위 : 지난달 1일 00시 ~ 이번달1일 00시

## How to Use (사용자)
- 슬랙의 PAY_EXCEL_BOT => 앱 세부정보
- 1-1. 서버를 켜는 URL로 접속
- 1-2. Lambda 스케쥴러가 서버를 매일 오전6시에 정지시킴
- 2... 결제내역, 인명부, 채널 ID 입력 창 접속
- 3... 기다리면 봇이 메시지로 진행상황/결과물 전송


## How to Deploy
- main에 push (github action)
- **주의사항** EC2 인스턴스가 꺼져있으면 Code Deploy가 실행에 실패하므로, 꼭 인스턴스를 켠 후 배포할 것


## requirements
- python 3.10
- requirements.txt
- env: 슬랙봇 토큰, 채널ID, 슬랙 리포트 채널 ID

## 추가 필요 작업
- 더 정밀하게 INPUT/OUTPUT 받아서 일을 더 줄여주기
- 비동기/Thread 화하기 -> API로 도중호출/정지 기능 추가
- SSLError 해결(*)
- DEPRECATED : 셀 목록 안쓰기로 해서 삭제
- TODO : 주차장 관련 댓글 저장 안되고 있음
