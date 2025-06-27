from src.core.models.rental_summary_contract import RentalSummaryContract


class SummaryService:

    def __init__(self, rental_summary_contract: RentalSummaryContract):
        self.rental_summary_contract = rental_summary_contract

    def process_summary(self):
        return {
            "CNPJ": self.rental_summary_contract.rental_contract.cnpj.formatted,
            "Razão Social": self.rental_summary_contract.rental_contract.name,
            "Geração Prevista": self.rental_summary_contract.predicted_generation,
            "Valor Contrato": self.rental_summary_contract.rental_contract.rent_value,
            "kWh Injetado": self.rental_summary_contract.injected_kwh,
            "kWh compensado": self.rental_summary_contract.compensated_kwh,
            "porcentagem compensada": self.rental_summary_contract.percent_compensated,
            "valor aluguel": self.rental_summary_contract.rent,
            "porcentagem injetada": self.rental_summary_contract.percent_injected,
            "month_reference": self.rental_summary_contract.month_reference,
        }
