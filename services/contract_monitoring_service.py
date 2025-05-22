from utils.cnpj import CNPJ
from repositories.sheets_repository import GoogleSheetsRepository


class ContractMonitoringService:

    def __init__(self, sheets_repo: GoogleSheetsRepository):
        self.sheets_repo = sheets_repo

    def get_cnpjs(self, column):
        valid_cnpjs = []
        for cnpj in self.sheets_repo.get_column(column):
            try:
                valid_cnpjs.append(CNPJ(cnpj))
            except:
                print("INVALID CNPJS:", cnpj)
                pass

        return valid_cnpjs
