from abc import ABC, abstractmethod

from src.core.models.bill import Bill


class BillRepository(ABC):

    @abstractmethod
    def get_bills_by_contracts_and_month(self, all_account_contracts, reference_month) -> list[Bill]:

        pass
