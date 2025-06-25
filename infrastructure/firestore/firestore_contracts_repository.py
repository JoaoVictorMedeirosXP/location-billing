from datetime import datetime

from google.cloud import firestore
from google.oauth2 import service_account
from config.settings import SERVICE_ACCOUNT_FILE

from models.rental_contract import RentalContract
from repositories.contracts_repository import ContractRepository
from utils.cnpj import CNPJ

from typing import List, Dict


class FirestoreContractsRepository(ContractRepository):
    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE
        )
        self.client = firestore.Client(credentials=credentials)

    def get_contracts_by_cnpjs(self, cnpjs: list):
        contracts_data = []
        chunk_size = 10

        for i in range(0, len(cnpjs), chunk_size):
            chunk = cnpjs[i : i + chunk_size]
            query = self.client.collection("rentalContracts").where("cnpj", "in", chunk)

            docs = query.stream()
            for doc in docs:
                contracts_data.append(doc.to_dict())

        return contracts_data

    def get_contracts_by_cnpj_and_date(self, cnpj_list, target_date):

        target_date_dt = datetime.strptime(target_date, "%Y-%m-%d").date()
        latest_by_cnpj = {}

        contracts_data = self.get_contracts_by_cnpjs(
            [cnpj.numbered for cnpj in cnpj_list]
        )

        for contract in contracts_data:
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
