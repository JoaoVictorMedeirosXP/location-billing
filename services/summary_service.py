from models.rental_contract import RentalContract

class Summary:
  
  def __init__(self, rental_contract: RentalContract):
    self.rental_contract = rental_contract
    
  def process_summary(self):
    summay = {
      "CNPJ": self.rental_contract.cnpj.formatted,
      "Razão Social": "",
      "Geração Prevista": "",
      "Valor Contrato": "",
      "kWh Injetado": "",
      "kWh compensado": "",
      "porcentagem compensada": "",
      "valor aluguel": "",
      "porcentagem injetada": ""
    }
    
    
    return
  