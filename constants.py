SLACK_URL = "https://humanscape.slack.com/api/"

PEOPLE_LIST_HEADERS = {
    "이름": "kor_name",
    "cic": "cic_name",
    "cell": "cell_name",
    "영어이름": "eng_name",
    "카드번호": "card_full_num",
}

WS_NEW_HEADERS = [
    "_",
    "승인일",
    "승인시간",
    "가맹점명",
    "가맹점사업자번호",
    "내용",
    "유형",
    "공급가액",
    "세액",
    "봉사료",
    "승인금액",
    "공제여부",
    "거래거분",
    "비고",
    "계정과목",
    "과세유형",
    "업종",
    "승인번호",
    "카드번호",
    "이용자명",
    "소지자",
    "CIC",
    "셀",
]
PAY_CHANNEL_NOT_CRAWL_LIST = [
    "스레드 누락 건입니다!",
    "has joined the channel",
    "예외 이체 요청 알림",
    "사용취소",
]
