from datetime import datetime

from src.adapters.firestore.connection import FirestoreClientSingleton
from src.core.models.rental_contract import RentalContract
from src.core.repositories.contracts_repository import ContractRepository
from src.utils.social_document import SocialNumber


class FirestoreContractsRepository(ContractRepository):
    def __init__(self):
        self.client = FirestoreClientSingleton.get_client()

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

    def get_contracts_by_cnpj_and_date(
        self, cnpj_list: list, target_date
    ) -> list[RentalContract]:

        target_date_dt = datetime.strptime(target_date, "%Y-%m-%d").date()
        latest_by_cnpj = {}

        contracts_data = self.get_contracts_by_cnpjs(
            [cnpj.numbered for cnpj in cnpj_list]
        )

        for contract in contracts_data:
            cnpj = SocialNumber(contract["cnpj"])
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

    def make_rental_contract(self, contract: dict) -> RentalContract:

        return RentalContract(
            calculation_method=contract["calculationMethod"],
            name=contract["name"],
            contractDate=contract["contractDate"],
            rent_value=self.set_rent_value(float(contract["rentValue"])),
            cnpj=SocialNumber(contract["cnpj"]),
            units=contract["units"],
            rental_units=contract["rentalUnits"],
        )

    def set_rent_value(self, rent_value: float) -> float:
        if not isinstance(rent_value, float):
            return 0
        return rent_value

    def get_all_contracts_cnpjs(self):
        return super().get_all_contracts_cnpjs()
