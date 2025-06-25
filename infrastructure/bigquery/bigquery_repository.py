from google.cloud import bigquery
from google.oauth2 import service_account
from config.settings import SERVICE_ACCOUNT_FILE

from models.bill import Bill
from repositories.bills_repository import BillRepository

from typing import List


class BigQueryBillsRepository(BillRepository):
    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE
        )
        self.client = bigquery.Client(credentials=credentials)

    def run_query(self, query: str):
        return self.client.query(query).to_dataframe()

    def get_bills_dataframe(self, all_account_contracts: List[str], reference_month):
        query = f"""
            SELECT *
            FROM `xperesidencial.big_data.bills_big_data` 
            WHERE mes_referencia = '{reference_month}'
            AND conta_contrato IN UNNEST({all_account_contracts})
        """
        return self.run_query(query)

    def get_bills(
        self, all_account_contracts: List[str], reference_month
    ) -> List[Bill]:
        bills_data = self.get_bills_dataframe(all_account_contracts, reference_month)
        return [Bill(**row.to_dict()) for _, row in bills_data.iterrows()]
