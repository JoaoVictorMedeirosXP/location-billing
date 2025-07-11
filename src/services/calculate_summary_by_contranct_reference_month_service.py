from src.core.models.rental_contract import RentalContract
from src.core.models.rental_summary_contract import RentalSummaryContract
from src.core.repositories.bills_repository import BillRepository
from src.utils.reference_month import ReferenceMonth


class calculateSummaryByContranctReferenceMonthService:

    def __init__(self, bills_repo: BillRepository):
        self.bills_repo = bills_repo

    def execute(
        self, rental_contract: RentalContract, reference_month: ReferenceMonth
    ) -> RentalSummaryContract:

        bills = self.bills_repo.get_bills_by_contracts_and_month(
            all_account_contracts=rental_contract.all_contract_codes,
            reference_month=reference_month,
        )

        unit_accounts = [unit["CONTA CONTRATO"] for unit in rental_contract.units]
        rental_unit_accounts = [
            unit["CONTA CONTRATO"] for unit in rental_contract.rental_units
        ]

        return RentalSummaryContract(
            rental_contract=rental_contract,
            month_reference=reference_month,
            units_bills=[
                bill for bill in bills if bill.conta_contrato in unit_accounts
            ],
            rental_units_bills=[
                bill for bill in bills if bill.conta_contrato in rental_unit_accounts
            ],
        )
