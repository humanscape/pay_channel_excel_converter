from datetime import datetime, timedelta

_now = datetime.now()
_month_ago = _now - timedelta(days=30)

SLACK_URL = "https://humanscape.slack.com/api/" 
START_AT = datetime(_month_ago.year,_month_ago.month,1)
END_AT = datetime(_now.year,_now.month,1)

YEAR = _month_ago.year
WS_NEW_HEADERS = ["_", "승인일","승인시간","가맹점명", "가맹점사업자번호", "내용", "유형", "공급가액", "세액", 
"봉사료","승인금액", "공제여부", "거래거분", "비고", "계정과목", "과세유형", "업종", "승인번호", "카드번호", 
"이용자명", "소지자", "CIC", "셀", "댓글/파일"]
PAY_CHANNEL_NOT_CRAWL_LIST = ["스레드 누락 건입니다!", "has joined the channel", "예외 이체 요청 알림", "사용취소"]