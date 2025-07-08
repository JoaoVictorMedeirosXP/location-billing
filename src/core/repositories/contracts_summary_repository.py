from abc import ABC, abstractmethod


class ContractSummaryRepository(ABC):

    @abstractmethod
    def append_write_contracts_summary(self):
        pass
    
    @abstractmethod
    def overwrite_contracts_summary(self):
        pass
