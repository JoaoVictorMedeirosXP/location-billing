from config.settings import SPREADSHEET_URL
from src.adapters.sheets.connection import SheetsClientSingleton
from src.core.repositories.contracts_repository import ContractRepository


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

    def get_all_contracts(self) -> list[dict]:
        all_values = self.sheet.get_all_values()

        if not all_values or len(all_values) < 2:
            return []

        header = [col.strip() for col in all_values[0]]
        header = [h for h in header if h]

        data_rows = all_values[1:]

        contracts = []
        for row in data_rows:
            if not any(cell.strip() for cell in row):
                continue

            row_dict = {
                header[i]: (row[i].strip() if i < len(row) else "")
                for i in range(len(header))
            }
            contracts.append(row_dict)

        return contracts

    def get_contract_by_id(self, id: int) -> dict | None:
        ids_column = self.get_column("A")

        ids_without_header = ids_column[1:]  

        try:
            row_idx_without_header = ids_without_header.index(str(id))
        except ValueError:
            return None

        row_index = row_idx_without_header + 2

        header = [col.strip() for col in self.sheet.row_values(1)]
        header = [h for h in header if h]

        row_values = self.sheet.row_values(row_index)

        row_dict = {
            header[i]: (row_values[i].strip() if i < len(row_values) else "")
            for i in range(len(header))
        }

        return row_dict
