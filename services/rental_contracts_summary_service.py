from models.rental_summary_contract import RentalSummaryContract
from models.rental_contract import RentalContract
from utils.date import reference_month
from repositories.bills_repository import BillRepository
from repositories.contracts_repository import ContractRepository

from typing import List


class RentalSummaryContractsService:

    def __init__(self, contracts_repo: ContractRepository, bills_repo: BillRepository):
        self.contracts_repo = contracts_repo
        self.bills_repo = bills_repo
        return

    def execute(
        self, cnpj_list: List[str], target_date: str
    ) -> List[RentalSummaryContract]:

        contracts_by_date_and_cnpj = self.contracts_repo.get_contracts_by_cnpj_and_date(
            cnpj_list=cnpj_list, target_date=target_date
        )

        return [
            self.make_rental_summary_contract(i, target_date=target_date)
            for i in contracts_by_date_and_cnpj
        ]

    def make_rental_summary_contract(
        self, rental_contract: RentalContract, target_date
    ) -> RentalSummaryContract:

        bills = self.bills_repo.get_bills(
            rental_contract.all_contract_codes,
            reference_month=reference_month(target_date),
        )
        
        unit_accounts = [unit["contractAccount"] for unit in rental_contract.units]
        rental_unit_accounts = [
            unit["contractAccount"] for unit in rental_contract.rental_units
        ]

        return RentalSummaryContract(
            rental_contract=rental_contract,
            units_bills=[
                bill
                for bill in bills
                if bill.conta_contrato in unit_accounts
            ],
            rental_units_bills=[
                bill
                for bill in bills
                if bill.conta_contrato in rental_unit_accounts
            ],
            month_reference=reference_month(target_date),
        )
