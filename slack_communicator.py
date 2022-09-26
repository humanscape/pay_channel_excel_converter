import os
import traceback
from asyncio import sleep
from collections import deque
from datetime import datetime
import urllib3
from requests.exceptions import SSLError

import requests

from common import NotWantToSaveException
from constants import START_AT, END_AT, SLACK_URL, PAY_CHANNEL_NOT_CRAWL_LIST
from schemas import ConversationsHistory, ConversationsReplies, SlackMessage

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
PAY_CHANNEL_ID = os.environ.get("PAY_CHANNEL_ID")
SLACK_REPORT_CHANNEL_ID = os.environ.get("SLACK_REPORT_CHANNEL_ID")

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def datetime_to_ts(_datetime: datetime):
    return _datetime.timestamp()


# 메시지 크롤링 dump 저장
class PayChannelData:
    # attr 정리
    card_company = ""
    card_num = ""
    pay_to = ""
    amount = ""
    country = ""
    replies = ""
    dict_key = ""

    def __init__(self, message: SlackMessage):
        """결제채널에 올라온 텍스트 데이터를 필요한 것들만 갖는 클래스로 변환"""
        text = message.text
        # text = "국민(8886) / 사용 / 28,000원 / 08/02 20:27 / 이태리부대찌개"
        if any(exec in text for exec in PAY_CHANNEL_NOT_CRAWL_LIST):
            raise NotWantToSaveException(text[:40])

        texts = list(map(str.strip, text.split("/")))
        # texts = ["국민(8886)", "사용", "28,000원", "08", "02 20:27", "이태리부대찌개"]

        if "(" in texts[2]:
            # KRW, USD 등 화폐/국가 표시된 경우 : 해외 결제건 - 제외
            raise NotWantToSaveException(texts[2])

        self.replies = []
        self.pay_to = texts[5]
        self.card_company, card_num = texts[0].split("(")
        self.card_num = card_num[:-1]

        year = START_AT.year
        month = texts[3]
        day, time = texts[4].split(" ")
        hour, minute = time.split(":")

        self.date_time = datetime(year, int(month), int(day), int(hour), int(minute))
        self.amount = texts[2][:-1].replace(",", "")

        self.dict_key = (
            f"{year}.{month}.{day} {hour}:{minute}:00 {self.card_num} {self.amount}"
        )

        def __repr__(self):
            return f"{self.card_company}({self.card_num}) {self.amount} {self.pay_to}"

    def __repr__(self):
        return f"{self.date_time} {self.card_num} {self.amount} {self.pay_to}"


class Slack:
    def __init__(self):
        self.Q1 = deque(["_"])
        self.pay_channel_datas = {}  # key:ts, value: PayChannelData
        self._data = {
            "channel": PAY_CHANNEL_ID,
        }
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        }

    def _post_(
        self,
        method: str,
        header_option: dict | None = None,
        data_option: dict | None = None,
    ):
        try:
            res = requests.post(
                url=SLACK_URL + method,
                headers={**self.headers, **header_option},
                data={**self._data, **data_option},
                verify=False,
            ).json()
            return res
        except SSLError as ssl_error:
            pass
            # await sleep(30)
            # self.error_report(ssl_error)

    def crawl_all_messages(self) -> dict:
        while self.Q1:
            cursor = self.Q1.popleft()
            if cursor == "_":
                self.save_300_message()
                continue
            self.save_300_message(cursor)

        return self.pay_channel_datas

    def save_300_message(self, cursor: str = None):
        res = ConversationsHistory(
            **self._post_(
                "conversations.history",
                data_option={
                    "cursor": cursor,
                    "oldest": datetime_to_ts(START_AT),
                    "latest": datetime_to_ts(END_AT),
                    "limit": 300,
                },
            )
        )
        for message in res.messages:
            try:
                self.pay_channel_datas[message.ts] = PayChannelData(message)
            except NotWantToSaveException as e:
                continue
            except BaseException as e:
                error_traceback = traceback.format_exc()
                self.error_report(error_traceback)
                continue

        if res.response_metadata:
            self.Q1.append(res.response_metadata.next_cursor)
        await sleep(3)
        return

    def get_a_reply_from_slack(self, ts, pay_channel_datas: dict):
        res = ConversationsReplies(
            **self._post_("conversations.replies", data_option={"ts": ts})
        )
        replies = pay_channel_datas[ts].replies

        for message in res.messages[1:]:
            replies.append(message.text)
            if message.files:
                replies.extend([file.permalink for file in message.files])
        return pay_channel_datas

    def send_file(self, file, channel_id: str):
        res = requests.post(
            url=f"{SLACK_URL}files.upload",
            headers=self.headers,
            data={
                "channels": channel_id,
                "content": file,
                "file": "bytes",
                "filename": "test2.xlsx",
                "filetype": "xlsx",
            },
        )
        print(res.json())

        return

    def error_report(self, message=traceback.format_exc()):
        res = self._post_(
            "chat.postMessage",
            data_option={
                "channel": SLACK_REPORT_CHANNEL_ID,
                "text": message,
            })

    def send_message(self, message: str, channel_id: str):
        res = self._post_(
            "chat.postMessage",
            data_option={"channel": channel_id, "text": message}
        )

        return res["ok"]
