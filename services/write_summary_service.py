import pandas as pd
from typing import List, Dict

from repositories.contracts_summary_repository import ContractSummaryRepository
from utils.reference_month import ReferenceMonth


class SheetsWriterService:

    def __init__(self, contract_summary_repo: ContractSummaryRepository):
        self.contract_summary_repo = contract_summary_repo

    def append_table_with_header(self, data: List[Dict]):
        if not data:
            print("Empty list")
            return

        df = pd.DataFrame(data)

        month_reference = ReferenceMonth(data[0]["month_reference"])

        df = df.drop(columns=["month_reference"])

        self.contract_summary_repo.write_contracts_summary(df, month_reference)

        return
