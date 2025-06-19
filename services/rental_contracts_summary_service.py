from models.rental_summary_contract import RentalSummaryContract
from models.rental_contract import RentalContract
from models.bill import Bill
from utils.cnpj import CNPJ
from utils.date import reference_month
from repositories.bigquery_repository import BigQueryRepository
from repositories.firestore_repository import FirestoreRepository

from datetime import datetime
from typing import List, Dict


class RentalSummaryContractsService:

    def __init__(
        self, firestore_repo: FirestoreRepository, big_query_repo: BigQueryRepository
    ):
        self.firestore_repo = firestore_repo
        self.big_query_repo = big_query_repo
        return

    def execute(
        self, cnpj_list: List[str], target_date: str
    ) -> List[RentalSummaryContract]:
        contracts_data = self.firestore_repo.get_contracts_by_cnpjs(
            [cnpj.numbered for cnpj in cnpj_list]
        )

        latest_contracts = self.get_contracts_by_cnpj_and_date(
            contracts_data, target_date
        )

        return [
            self.make_rental_summary_contract(i, target_date=target_date)
            for i in latest_contracts
        ]

    def get_contracts_by_cnpj_and_date(
        self, contracts: List[Dict], target_date: str
    ) -> List[RentalContract]:
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

        return list(
            [
                self.make_rental_contract(contract)
                for contract in latest_by_cnpj.values()
            ]
        )

    def make_rental_contract(self, contract: Dict) -> RentalContract:

        return RentalContract(
            calculation_method=contract["calculationMethod"],
            name=contract["name"],
            contractDate=contract["contractDate"],
            rent_value=self.set_rent_value(contract["rentValue"]),
            cnpj=CNPJ(contract["cnpj"]),
            units=contract["units"],
            rental_units=contract["rentalUnits"],
        )

    def set_rent_value(self, rent_value):
        try:
            return float(rent_value)
        except:
            return 0

    def make_rental_summary_contract(
        self, rental_contract: RentalContract, target_date
    ) -> RentalSummaryContract:

        bills = self.get_bills(
            rental_contract.all_contract_codes,
            reference_month=reference_month(target_date),
        )
        
        return RentalSummaryContract(
            rental_contract=rental_contract,
            units_bills=[
                Bill(**row.to_dict())
                for _, row in bills[
                    bills["conta_contrato"].isin([i['contractAccount'] for i in rental_contract.units])
                ].iterrows()
            ],
            rental_units_bills=[
                Bill(**row.to_dict())
                for _, row in bills[
                    bills["conta_contrato"].isin([i['contractAccount'] for i in rental_contract.rental_units])
                ].iterrows()
            ],
            month_reference=reference_month(target_date),
        )

    def get_bills(self, all_account_contracts, reference_month):
        query = f"""
            SELECT *
            FROM `xperesidencial.big_data.bills_big_data` 
            WHERE mes_referencia = '{reference_month}'
            AND conta_contrato IN UNNEST({all_account_contracts})
        """
        return self.big_query_repo.run_query(query)
