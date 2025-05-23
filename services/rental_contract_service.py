from models.rental_contract import RentalContract
from models.bill import Bill
from utils.cnpj import CNPJ
from utils.date import reference_month
from repositories.bigquery_repository import BigQueryRepository
from repositories.firestore_repository import FirestoreRepository

from datetime import datetime
from typing import List, Dict


class RentalContractService:

    def __init__(
        self, firestore_repo: FirestoreRepository, big_query_repo: BigQueryRepository
    ):
        self.firestore_repo = firestore_repo
        self.big_query_repo = big_query_repo
        return

    def process_rental_contracts(self, cnpj_list: List[str], target_date: str):
        contracts_data = self.firestore_repo.get_contracts_by_cnpjs(
            [cnpj.numbered for cnpj in cnpj_list]
        )

        latest_contracts = self.get_latest_contracts_by_cnpj(
            contracts_data, target_date
        )

        return [
            self.set_contract_with_bills(i, target_date=target_date)
            for i in latest_contracts
        ]

    def get_latest_contracts_by_cnpj(self, contracts: List[Dict], target_date: str):
        target_date_dt = datetime.strptime(target_date, "%Y-%m-%d").date()
        latest_by_cnpj = {}

        for contract in contracts:
            cnpj = CNPJ(contract["cnpj"])
            contract_date = contract["contractDate"].date()

            if contract_date <= target_date_dt:
                if (
                    cnpj not in latest_by_cnpj
                    or contract_date > latest_by_cnpj[cnpj]["contractDate"].date()
                ):
                    latest_by_cnpj[cnpj] = contract

        return list(latest_by_cnpj.values())

    def set_rent_value(self, rent_value):
        try:
            return float(rent_value)
        except:
            return 0

    def set_contract_with_bills(self, contract, target_date):
        units = [i["contractAccount"] for i in contract["units"]]
        rental_units = [i["contractAccount"] for i in contract["rentalUnits"]]
        bills = self.get_bills(
            units + rental_units, reference_month=reference_month(target_date)
        )
        return RentalContract(
            contractDate=contract["contractDate"],
            name=contract["name"],
            rent_value=self.set_rent_value(contract["rentValue"]),
            calculation_method=contract["calculationMethod"],
            cnpj=CNPJ(contract["cnpj"]),
            units=contract["units"],
            rental_units=contract["rentalUnits"],
            units_bills=[
                Bill(**row.to_dict())
                for _, row in bills[bills["conta_contrato"].isin(units)].iterrows()
            ],
            rental_units_bills=[
                Bill(**row.to_dict())
                for _, row in bills[
                    bills["conta_contrato"].isin(rental_units)
                ].iterrows()
            ],
            month_reference=reference_month(target_date)
        )

    def get_bills(self, all_account_contracts, reference_month):
        query = f"""
            SELECT *
            FROM `xperesidencial.big_data.bills_big_data` 
            WHERE mes_referencia = '{reference_month}'
            AND conta_contrato IN UNNEST({all_account_contracts})
        """
        return self.big_query_repo.run_query(query)
