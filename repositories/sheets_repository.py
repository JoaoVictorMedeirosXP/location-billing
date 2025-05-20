import gspread
import pandas as pd
from gspread_dataframe import set_with_dataframe
from google.oauth2 import service_account
from config.settings import SERVICE_ACCOUNT_FILE, SPREADSHEET_URL, SHEET_NAME, NUM_ROWS_TO_JUMP

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

class GoogleSheetsRepository:
    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=SCOPES
        )
        self.gc = gspread.authorize(credentials)
        self.sheet = self.gc.open_by_url(SPREADSHEET_URL).worksheet(SHEET_NAME)

    def get_next_rows(self) -> int:
        return len(self.sheet.get_all_values()) + NUM_ROWS_TO_JUMP

    def append_dataframe(self, df: pd.DataFrame):
        row = self.get_next_rows()
        set_with_dataframe(self.sheet, df, row=row, include_column_header=False)
