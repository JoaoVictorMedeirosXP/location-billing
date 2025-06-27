import pandas as pd
from adapters.sheets.connection import SheetsClientSingleton
from config.settings import (
    NUM_ROWS_TO_JUMP,
    SPREADSHEET_URL,
)
from gspread_dataframe import set_with_dataframe
from repositories.contracts_summary_repository import ContractSummaryRepository
from utils.reference_month import ReferenceMonth


class SheetsContractSummaryRepository(ContractSummaryRepository):

    def __init__(self, work_sheet):
        self.client = SheetsClientSingleton.get_client()
        self.sheet = self.client.open_by_url(SPREADSHEET_URL).worksheet(work_sheet)

    def get_next_rows(self) -> int:
        return len(self.sheet.get_all_values()) + NUM_ROWS_TO_JUMP

    def write_contracts_summary(
        self, df: pd.DataFrame, month_reference: ReferenceMonth
    ):
        row = self.get_next_rows()

        self.sheet.update(
            f"A{row}", [[f"Mês de referência: {month_reference.as_string}"]]
        )

        set_with_dataframe(self.sheet, df, row=row + 1, include_column_header=True)
