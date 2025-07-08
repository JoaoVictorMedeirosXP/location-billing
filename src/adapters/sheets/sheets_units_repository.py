from config.settings import SPREADSHEET_URL
from src.adapters.sheets.connection import SheetsClientSingleton
from src.core.repositories.units_repository import UnitsRepository


class SheetsUnitsRepository(UnitsRepository):

    def __init__(self, work_sheet):
        self.client = SheetsClientSingleton.get_client()
        self.sheet = self.client.open_by_url(SPREADSHEET_URL).worksheet(work_sheet)

    def _get_column(self, column_letter: str):
        col_index = ord(column_letter.upper()) - ord("A") + 1
        column_values = self.sheet.col_values(col_index)
        non_null_values = [value.strip() for value in column_values if value.strip() != ""]
        return non_null_values

    def check_unit_by_account_contract(self, account_contract: str) -> bool:
        account_contracts = self._get_column("C")
        return account_contract in account_contracts

    def get_units_by_contract_id(self, contract_id: str) -> list[dict]:

        all_values = self.sheet.get_all_values()

        if not all_values or len(all_values) < 2:
            return []

        header = [col.strip() for col in all_values[0]]
        header = [h for h in header if h]

        data_rows = all_values[1:]

        try:
            contract_id_index = header.index("ID DO CONTRATO")
        except ValueError:
            raise ValueError("Coluna 'ID DO CONTRATO' não encontrada na planilha")

        result = []
        for row in data_rows:
            if len(row) <= contract_id_index:
                continue
            if row[contract_id_index].strip() == contract_id:
                row_dict = {header[i]: (row[i].strip() if i < len(row) else "") for i in range(len(header))}
                result.append(row_dict)

        return result
