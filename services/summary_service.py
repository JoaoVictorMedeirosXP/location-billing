from models.rental_contract import RentalContract


class SummaryService:

    def __init__(self, rental_contract: RentalContract):
        self.rental_contract = rental_contract

    def process_summary(self):
        return {
            "CNPJ": self.rental_contract.cnpj.formatted,
            "Razão Social": self.rental_contract.name,
            "Geração Prevista": self.rental_contract.predicted_generation,
            "Valor Contrato": self.rental_contract.rent_value,
            "kWh Injetado": self.rental_contract.injected_kwh,
            "kWh compensado": self.rental_contract.compensated_kwh,
            "porcentagem compensada": self.rental_contract.percent_compensated,
            "valor aluguel": self.rental_contract.rent,
            "porcentagem injetada": self.rental_contract.percent_injected,
        }
