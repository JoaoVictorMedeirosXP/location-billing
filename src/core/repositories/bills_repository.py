from abc import ABC, abstractmethod

from src.core.models.bill import Bill


class BillRepository(ABC):

    @abstractmethod
    def get_bills(self, all_account_contracts, reference_month) -> list[Bill]:

        pass
