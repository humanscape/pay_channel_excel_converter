from typing import Tuple
import openpyxl


class Human:
    def __init__(
        self, cic_name, cell_name, kor_name, eng_name, card_full_num, nicknames=[]
    ):
        self.cic_name = cic_name
        self.cell_name = cell_name
        self.eng_name = eng_name
        self.kor_name = kor_name
        self.card_full_num = card_full_num
        self.nicknames = nicknames

    def __repr__(self):
        return f"{self.cic_name} {self.cell_name} {self.eng_name}"


class NameExcelToDict:
    header_cols = {"nicknames": []}
    HEADER_START_ROW = 2

    def run(self, wb_people: openpyxl.Workbook) -> Tuple[dict, dict]:
        ws = wb_people["Member List"]
        self._set_headers(ws)
        nick_to_human, card_num_to_human = self._make_human_dict(ws)

        return nick_to_human, card_num_to_human

    def _set_headers(self, ws):
        HEADERS = {
            "이름": "kor_name",
            "cic": "cic_name",
            "cell": "cell_name",
            "영어이름": "eng_name",
            "카드번호": "card_full_num",
        }
        headers = ws[self.HEADER_START_ROW]
        for header in headers:
            if header.value is None:
                continue
            value = header.value.lower()
            if value in HEADERS:
                self.header_cols[HEADERS[value]] = header.col_idx
            elif "name" in value:
                self.header_cols["nicknames"].append(header.col_idx)

    def _get_id_num(self, ws, row):
        return ws.cell(row, 1).value

    def _make_human_dict(self, ws):
        row = self.HEADER_START_ROW + 1
        nick_to_human = {}
        card_num_to_human = {}
        while self._get_id_num(ws, row) is not None:
            row_values = {}
            for header, col_nums in self.header_cols.items():
                if header == "nicknames":
                    continue
                row_values[header] = ws.cell(row, col_nums).value
            for nickname_cols in self.header_cols["nicknames"]:
                nickname = ws.cell(row, nickname_cols).value
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
