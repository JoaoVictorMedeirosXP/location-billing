import pandas as pd
from repositories.sheets_repository import GoogleSheetsRepository


class SheetsWriterService:

    def __init__(self, sheets_repo: GoogleSheetsRepository):
        self.sheets_repo = sheets_repo

    def append_table_with_header(self, data: list[dict]):
        if not data:
            print("Empty list")
            return

        df = pd.DataFrame(data)

        self.sheets_repo.append_dataframe(df)

        return
