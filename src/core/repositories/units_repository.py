from abc import ABC, abstractmethod


class UnitsRepository(ABC):

    @abstractmethod
    def check_unit_by_account_contract(self, account_contract) -> bool:
        pass
