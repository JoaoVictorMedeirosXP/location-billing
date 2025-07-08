from src.core.repositories.units_repository import UnitsRepository


class CheckUnitIsGdService:
    
    
    def __init__(self, units_repo: UnitsRepository):
        self.units_repo = units_repo
        
    def execute(self, contract_acount: str) -> bool:
        return self.units_repo.check_unit_by_account_contract(contract_acount)

    