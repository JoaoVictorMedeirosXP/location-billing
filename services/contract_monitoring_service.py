from utils.cnpj import CNPJ

class ContractMonitoringService:
    
    def __init__(self, sheets_repo):
        self.sheets_repo = sheets_repo
        
    def get_cnpjs(self, column):
        valid_cnpjs = []
        for i in self.sheets_repo.get_column(column):
            try:
                valid_cnpjs.append(CNPJ(i))
            except:
                pass
        
        return valid_cnpjs
