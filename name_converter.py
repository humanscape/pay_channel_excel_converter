from typing import Tuple, Final, Dict, List
import openpyxl
from pydantic import BaseModel

from constants import PEOPLE_LIST_HEADERS


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
        self.nick_to_human = {}
        self.card_num_to_human = {}

    def run(self) -> Tuple[dict, dict]:
        self._init_cols()
        self._make_human_dict()

        return self.nick_to_human, self.card_num_to_human

    def _init_cols(self):
        header_cells = self.ws[self.HEADER_START_ROW]
        for cell in header_cells:
            if cell.value is None:
                continue
            value = cell.value.lower()
            self._set_header_cols(cell, value)
            self._set_nickname_cols(cell, value)

    def _set_header_cols(self, cell, value):
        if value in PEOPLE_LIST_HEADERS:
            self.header_cols[PEOPLE_LIST_HEADERS[value]] = cell.col_idx

    def _set_nickname_cols(self, cell, value):
        if "name" in value:
            self.header_cols["nicknames"].append(cell.col_idx)

    def _get_id_num(self, row):
        return self.ws.cell(row, 1).value

    def _make_human_dict(self):
        row = self.HEADER_START_ROW + 1
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
                if nickname in self.nick_to_human:
                    self.nick_to_human[nickname] = False
                    continue
                human = Human(**row_values)
                self.nick_to_human[nickname] = human
                self.card_num_to_human[human.card_full_num] = human
            row += 1

        return

