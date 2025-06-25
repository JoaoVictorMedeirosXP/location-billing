from abc import ABC, abstractmethod

from models.bill import Bill
from typing import List


class BillRepository(ABC):

    @abstractmethod
    def get_bills(self, all_account_contracts, reference_month) -> List[Bill]:

        pass
