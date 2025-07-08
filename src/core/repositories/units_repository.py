from abc import ABC, abstractmethod


class UnitsRepository(ABC):

    @abstractmethod
    def check_unit_by_account_contract(self, account_contract) -> bool:
        pass

    @abstractmethod
    def get_units_by_contract_id(self, contract_id):
        pass
