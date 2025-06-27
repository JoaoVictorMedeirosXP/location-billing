from src.core.repositories.contracts_repository import ContractRepository
from src.utils.social_document import SocialNumber


class ContractMonitoringService:

    def __init__(self, contracts_repo: ContractRepository):
        self.contracts_repo = contracts_repo

    def get_cnpjs(self):
        valid_cnpjs = []
        for cnpj in self.contracts_repo.get_all_contracts_cnpjs():
            social_number = SocialNumber(cnpj)
            if social_number.is_valid():
                valid_cnpjs.append(social_number)

        return valid_cnpjs
