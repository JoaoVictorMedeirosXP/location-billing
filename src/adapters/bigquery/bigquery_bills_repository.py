from src.adapters.bigquery.connection import BigQueryClientSingleton
from src.core.models.bill import Bill
from src.core.repositories.bills_repository import BillRepository


class BigQueryBillsRepository(BillRepository):
    def __init__(self):
        self.client = BigQueryClientSingleton.get_client()

    def run_query(self, query: str):
        return self.client.query(query).to_dataframe()

    def get_bills_dataframe(self, all_account_contracts: list[str], reference_month):
        query = f"""
            SELECT *
            FROM `xperesidencial.big_data.bills_big_data` 
            WHERE mes_referencia = '{reference_month}'
            AND conta_contrato IN UNNEST({all_account_contracts})
        """
        return self.run_query(query)

    def get_bills(
        self, all_account_contracts: list[str], reference_month
    ) -> list[Bill]:
        bills_data = self.get_bills_dataframe(all_account_contracts, reference_month)
        return [Bill(**row.to_dict()) for _, row in bills_data.iterrows()]
