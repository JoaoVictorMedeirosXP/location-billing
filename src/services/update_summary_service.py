from src.core.models.rental_summary_contract import RentalSummaryContract
from src.core.repositories.contracts_summary_repository import ContractSummaryRepository


class updateSummaryService:

    def __init__(self, summary_repo: ContractSummaryRepository):

        self.summary_repo = summary_repo

    def execute(self, summary: RentalSummaryContract):

        self.summary_repo.update_summary_row_by_month_and_cnpj(
            self.make_processed_summary_service(summary=summary)
        )

    def make_processed_summary_service(self, summary: RentalSummaryContract) -> dict:

        return {
            "month": summary.month_reference.as_month_pt,
            "cnpj": summary.rental_contract.cnpj.formatted,
            "values": {
                "Razão Social": summary.rental_contract.name,
                "Geração Prevista": summary.predicted_generation,
                "Valor Contrato": summary.rental_contract.rent_value,
                "kWh Injetado": summary.injected_kwh,
                "kWh compensado": summary.compensated_kwh,
                "porcentagem compensada": summary.percent_compensated,
                "valor aluguel": summary.rent,
                "porcentagem injetada": summary.percent_injected,
                "Contas Emitidas": summary.emitted_bills,
            },
        }
