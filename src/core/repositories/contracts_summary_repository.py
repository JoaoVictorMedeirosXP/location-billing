from abc import ABC, abstractmethod


class ContractSummaryRepository(ABC):

    @abstractmethod
    def append_write_contracts_summary(self):
        pass
    
    @abstractmethod
    def update_summary_row_by_month_and_cnpj(self, update_data: dict):
        pass
    
    @abstractmethod
    def overwrite_contracts_summary(self):
        pass
