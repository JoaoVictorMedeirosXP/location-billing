from config.settings import (
    SPREADSHEET_URL
)
from adapters.sheets.connection import SheetsClientSingleton
from repositories.contracts_repository import ContractRepository

class SheetsContractsRepository(ContractRepository):

    def __init__(self, work_sheet):
        self.client = SheetsClientSingleton.get_client()
        self.sheet = self.client.open_by_url(SPREADSHEET_URL).worksheet(work_sheet)

    def get_column(self, column: str):
        column_values = self.sheet.col_values(ord(column.upper()) - ord("A") + 1)

        non_null_values = [value for value in column_values if value.strip() != ""]

        return non_null_values
    
    def get_all_contracts_cnpjs(self):
        return self.get_column("E")

    def get_contracts_by_cnpj_and_date(self, cnpj_list, target_date):
        return super().get_contracts_by_cnpj_and_date(cnpj_list, target_date)