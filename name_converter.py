from typing import Tuple, Final, Dict, List
import openpyxl
from pydantic import BaseModel


class Human(BaseModel):
    cic_name: str
    cell_name: str
    eng_name: str
    kor_name: str
    eng_name: str
    card_full_num: str | None

    def __repr__(self):
        return f"{self.cic_name} {self.cell_name} {self.eng_name}"


class NameExcelToDict:
    header_cols = {"nicknames": []}
    HEADER_START_ROW = 2

    def __init__(self, wb_people: openpyxl.Workbook):
        self.ws = wb_people["Member List"]

    def run(self) -> Tuple[dict, dict]:
        self._set_headers()
        nick_to_human, card_num_to_human = self._make_human_dict()

        return nick_to_human, card_num_to_human

    def _set_headers(self):
        HEADERS:Final = {
            "이름": "kor_name",
            "cic": "cic_name",
            "cell": "cell_name",
            "영어이름": "eng_name",
            "카드번호": "card_full_num",
        }
        headers = self.ws[self.HEADER_START_ROW]
        for header in headers:
            if header.value is None:
                continue
            value = header.value.lower()
            if value in HEADERS:
                self.header_cols[HEADERS[value]] = header.col_idx
            elif "name" in value:
                self.header_cols["nicknames"].append(header.col_idx)

    def _get_id_num(self, row):
        return self.ws.cell(row, 1).value

    def _make_human_dict(self):
        row = self.HEADER_START_ROW + 1
        nick_to_human = {}
        card_num_to_human = {}
        while self._get_id_num(row) is not None:
            row_values = {}
            for header, col_nums in self.header_cols.items():
                if header == "nicknames":
                    continue
                row_values[header] = self.ws.cell(row, col_nums).value
            for nickname_cols in self.header_cols["nicknames"]:
                nickname = self.ws.cell(row, nickname_cols).value
                if not nickname:
                    continue
                if nickname in nick_to_human:
                    nick_to_human[nickname] = False
                    continue
                human = Human(**row_values)
                nick_to_human[nickname] = human
                card_num_to_human[human.card_full_num] = human
            row += 1

        return nick_to_human, card_num_to_human
