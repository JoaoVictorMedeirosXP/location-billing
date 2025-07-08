
from src.adapters.firestore.firestore_bills_repository import FirestoreBillsRepository
from src.utils.reference_month import ReferenceMonth


def test_get_bills_by_contracts_and_month():

    bills_repository = FirestoreBillsRepository()

    all_account_contracts = ["7039033571", "7058415710"]
    reference_month = ReferenceMonth.current()

    bills = bills_repository.get_bills_by_contracts_and_month(
        reference_month=reference_month, all_account_contracts=all_account_contracts
    )

    print(bills)
