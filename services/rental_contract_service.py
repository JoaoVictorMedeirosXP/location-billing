from models.rental_contract import RentalContract
from models.bill import Bill
from utils.cnpj import CNPJ

from datetime import date


class RentalContractService:

    def __init__(self, firestore_repo, big_query_repo):
        self.firestore_repo = firestore_repo
        self.big_query_repo = big_query_repo
        return

    def process_active_contracts(self):
        firestore_cliente = self.firestore_repo()
        contracts_data = firestore_cliente.get_all_contracts()
        latest_contracts = self.get_latest_contracts_by_cnpj(contracts_data)
        return [self.set_contract_with_bills(i) for i in latest_contracts]

    def get_latest_contracts_by_cnpj(self, contracts):
        latest_by_cnpj = {}
        for contract in contracts:
            print(contract)
            cnpj = CNPJ(contract["cnpj"])
            if (
                cnpj not in latest_by_cnpj
                or contract["contractDate"] > latest_by_cnpj[cnpj]["contractDate"]
            ):
                latest_by_cnpj[cnpj] = contract
        return list(latest_by_cnpj.values())

    def set_contract_with_bills(self, contract):
        units = [i["contractAccount"] for i in contract["units"]]
        rental_units = [i["contractAccount"] for i in contract["rentalUnits"]]
        bills = self.get_bills(units + rental_units, date.today())

        return RentalContract(
            contractDate=contract["contractDate"],
            name=contract["name"],
            rentValue=contract["rentalValue"],
            calculationMethod=contract["calculationMethod"],
            units=[
                Bill(**row.to_dict())
                for _, row in bills[bills["conta_contrato"].isin(units)].iterrows()
            ],
            rental_units=[
                Bill(**row.to_dict())
                for _, row in bills[
                    bills["conta_contrato"].isin(rental_units)
                ].iterrows()
            ],
        )

    def get_bills(self, all_account_contracts, reference_month):
        bq = self.big_query_repo()
        query = """
            SELECT *
            FROM `xperesidencial.big_data.bills_big_data` 
            WHERE mes_referencia = ${reference_month}
            AND conta_contrato IN UNNEST(${all_account_contracts})
        """
        return bq.run_query(query)
