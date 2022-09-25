import traceback
from datetime import datetime
from asyncio import sleep
from io import BytesIO

from requests.exceptions import SSLError
from openpyxl import load_workbook
from openpyxl.writer.excel import save_virtual_workbook
from fastapi import FastAPI, UploadFile, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from name_converter import NameExcelToDict
from card_data_conveter import CardDataConverter
from slack_communicator import Slack
from constants import START_AT, END_AT

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def upload_form(request:Request):
    templates = Jinja2Templates(directory="templates")
    return templates.TemplateResponse("upload_form.html", {"request":request})

# @app.get("/stop")
# async def stop():
#     """플로우
#     진행중인 작업 중지
#     """

# @app.get("/time_check")
# async def time_check():
#     """플로우
#     기대 전체시간 = 전체 메시지 길이 * 3.3초
#     남은 기대시간 = (전체 메시지 길이 - 여태까지 긁어온 메시지 길이) * 3.3초
#     """


@app.post("/run/")
async def run(people_file: UploadFile, card_file:UploadFile, channel_id:str=Form()):
    slack = Slack()
    send_success = slack.send_message(f"요청을 받았습니다. 시작시간 :{datetime.now()} / 검색범위 : {START_AT} ~ {END_AT}",channel_id)
    if not send_success:
        return "슬랙 메시지 전송에 실패했습니다. 채널ID를 확인해주세요."

    people_file_read = await people_file.read()
    wb_people = load_workbook(filename=BytesIO(people_file_read))
    nick_to_human, card_num_to_human = NameExcelToDict().run(wb_people=wb_people)

    card_file_read = await card_file.read()
    wb_card = load_workbook(filename=BytesIO(card_file_read))
    card_data_converter = CardDataConverter(wb_card)
    card_sheet = card_data_converter.get_new_sheet()
    card_dict = card_data_converter.get_card_data_dict()
    card_data_converter.add_card_owner_to_new_sheet(card_num_to_human)

    attempts = 0
    pay_messages = None
    attempts += 1
    pay_messages = slack.crawl_all_messages()

    if pay_messages is None :
        slack.error_report(message="채널에서 메시지 수집에 실패했습니다.")
        return "채널에서 메시지 수집에 실패했습니다."
    attempts = 0
    idx_passed = 0

    while attempts < 50 :
        attempts += 1
        try : 
            for idx, (ts, pay_channel_data) in enumerate(pay_messages.items()):
                if (
                    (idx < idx_passed)
                    or 
                    (not pay_channel_data.dict_key in card_dict)
                ):
                    continue
                if idx%100 == 0 :
                    slack.send_message(f"{len(pay_messages)}개의 글 중 {idx}번째 글의 댓글 수집중", channel_id)
                slack.get_a_reply_from_slack(ts,pay_messages)
                row = card_dict[pay_channel_data.dict_key]

                if pay_channel_data.replies :
                    card_data_converter.add_comments(card_sheet, row, pay_channel_data)
                    card_data_converter.add_usage_and_owners(card_sheet, row, pay_channel_data, nick_to_human)
                idx_passed = idx
                await sleep(2)
            break
        except SSLError as ssl_error :
            slack.error_report(ssl_error)
        except BaseException as e:
            error_traceback = traceback.format_exc()
            slack.error_report(error_traceback)
    
    # 결과물 (OUTPUT)
    vb = save_virtual_workbook(wb_card)    
    slack.send_file(file=vb, channel_id=channel_id)
    return "슬랙 메시지를 확인하세요."
