from utils.social_document import SocialNumber
from repositories.contracts_repository import ContractRepository


class ContractMonitoringService:

    def __init__(self, contracts_repo: ContractRepository):
        self.contracts_repo = contracts_repo

    def get_cnpjs(self):
        valid_cnpjs = []
        for cnpj in self.contracts_repo.get_all_contracts_cnpjs():
            try:
                valid_cnpjs.append(SocialNumber(cnpj))
            except:
                print("INVALID CNPJS:", cnpj)
                pass

        return valid_cnpjs
