from abc import ABC, abstractmethod
 

class ContractSummaryRepository(ABC):
    
    @abstractmethod
    def write_contracts_summary(self):
        pass

