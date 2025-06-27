from abc import ABC, abstractmethod

from models.rental_contract import RentalContract


class ContractRepository(ABC):

    @abstractmethod
    def get_contracts_by_cnpj_and_date(
        self, cnpj_list: list[str], target_date: str
    ) -> list[RentalContract]:

        pass

    @abstractmethod
    def get_all_contracts_cnpjs(self):
        pass
