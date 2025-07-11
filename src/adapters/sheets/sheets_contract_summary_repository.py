import time

import pandas as pd
from config.settings import (
    NUM_ROWS_TO_JUMP,
    SPREADSHEET_URL,
)
from gspread_dataframe import set_with_dataframe
from src.adapters.sheets.connection import SheetsClientSingleton
from src.core.repositories.contracts_summary_repository import ContractSummaryRepository
from src.utils.reference_month import ReferenceMonth


class SheetsContractSummaryRepository(ContractSummaryRepository):

    DEFAULT_HEADER = [
        "CNPJ",
        "Razão Social",
        "Geração Prevista",
        "Valor Contrato",
        "kWh Injetado",
        "kWh compensado",
        "porcentagem compensada",
        "valor aluguel",
        "porcentagem injetada",
        "Contas Emitidas",
    ]

    def __init__(self, work_sheet: str):
        self.client = SheetsClientSingleton.get_client()
        self.sheet = self.client.open_by_url(SPREADSHEET_URL).worksheet(work_sheet)

    def get_next_rows(self) -> int:
        return len(self.sheet.get_all_values()) + NUM_ROWS_TO_JUMP

    def append_write_contracts_summary(
        self, df: pd.DataFrame, month_reference: ReferenceMonth
    ):
        row = self.get_next_rows()
        self.sheet.update(
            f"A{row}", [[f"Mês de referência: {month_reference.as_string}"]]
        )
        set_with_dataframe(self.sheet, df, row=row + 1, include_column_header=True)

    def overwrite_contracts_summary(self, df: pd.DataFrame):
        self.sheet.clear()
        set_with_dataframe(self.sheet, df, include_column_header=True)

    def create_new_section(self, month: str) -> None:
        """Cria nova seção com header padrão."""
        all_values = self.sheet.get_all_values()
        header_row = self.DEFAULT_HEADER

        insert_title_row_index = len(all_values) + 3

        batch_values = [
            [f"Cobrança {month}"],
            header_row,
        ]
        self.sheet.update(
            f"A{insert_title_row_index}:Z{insert_title_row_index + 1}", batch_values
        )

    def _wait_for_section(
        self, month: str, timeout: float = 10, interval: float = 0.5
    ) -> int:
        target_title = f"Cobrança {month}"
        start_time = time.time()

        while time.time() - start_time < timeout:
            all_values = self.sheet.get_all_values()
            for i, row in enumerate(all_values):
                if row and row[0].strip() == target_title:
                    if i + 1 < len(all_values):
                        header_row = all_values[i + 1]
                        if header_row and any(cell.strip() for cell in header_row):
                            return i + 1
            time.sleep(interval)

        raise TimeoutError(
            f"Seção '{target_title}' não apareceu na planilha após {timeout} segundos."
        )

    def update_summary_row_by_month_and_cnpj(self, update_data: dict):
        month = update_data["month"]
        cnpj = update_data["cnpj"].strip()
        values = update_data["values"]

        all_values = self.sheet.get_all_values()

        if not all_values:
            self.create_new_section(month)
            header_row_index = self._wait_for_section(month)
            all_values = self.sheet.get_all_values()
        else:
            target_title = f"Cobrança {month}"
            title_row_index = next(
                (
                    i
                    for i, row in enumerate(all_values)
                    if row and row[0].strip() == target_title
                ),
                None,
            )
            if title_row_index is None:
                self.create_new_section(month)
                header_row_index = self._wait_for_section(month)
                all_values = self.sheet.get_all_values()
            else:
                header_row_index = title_row_index + 1

        header_row = all_values[header_row_index]
        header_map = {
            col.strip(): idx + 1 for idx, col in enumerate(header_row) if col.strip()
        }

        if "CNPJ" not in header_map:
            raise ValueError("Coluna 'CNPJ' não encontrada no header da planilha.")

        cnpj_col_index = header_map["CNPJ"]

        current_row_index = header_row_index + 1
        while current_row_index < len(all_values):
            row = all_values[current_row_index]
            if all(cell.strip() == "" for cell in row):
                break
            if len(row) >= cnpj_col_index and row[cnpj_col_index - 1].strip() == cnpj:
                for column_name, new_value in values.items():
                    if column_name not in header_map:
                        raise ValueError(
                            f"Coluna '{column_name}' não existe no header da planilha."
                        )
                    col_index = header_map[column_name]
                    self.sheet.update_cell(current_row_index + 1, col_index, new_value)
                return
            current_row_index += 1

        insert_row_index = current_row_index + 1
        new_row = [""] * len(header_map)
        new_row[cnpj_col_index - 1] = cnpj

        for column_name, new_value in values.items():
            if column_name not in header_map:
                raise ValueError(
                    f"Coluna '{column_name}' não existe no header da planilha."
                )
            col_index = header_map[column_name]
            new_row[col_index - 1] = new_value

        self.sheet.insert_row(new_row, insert_row_index)
