from abc import ABC, abstractmethod
from models.rental_contract import RentalContract
from typing import List, Dict


class ContractRepository(ABC):

    @abstractmethod
    def get_contracts_by_cnpj_and_date(
        self, cnpj_list: List[str], target_date: str
    ) -> List[RentalContract]:

        pass
