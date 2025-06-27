from services.contract_monitoring_service import ContractMonitoringService
from services.rental_contracts_summary_service import RentalSummaryContractsService
from services.summary_service import SummaryService
from services.write_summary_service import SheetsWriterService


class ProcessContractsFromSheetUseCase:
    def __init__(
        self,
        rental_summary_service: RentalSummaryContractsService,
        monitoring_service: ContractMonitoringService,
        writer_service: SheetsWriterService,
        summary_service: SummaryService,
    ):
        self.rental_summary_service = rental_summary_service
        self.monitoring_service = monitoring_service
        self.writer_service = writer_service
        self.summary_service = summary_service

    def execute(self, target_date: str) -> int:
        print("Use case, process contracts from sheets")
        cnpjs = self.monitoring_service.get_cnpjs()

        rental_contracts = self.rental_summary_service.execute(
            cnpj_list=cnpjs, target_date=target_date
        )

        summaries = [
            self.summary_service(contract).process_summary()
            for contract in rental_contracts
        ]

        self.writer_service.append_table_with_header(data=summaries)

        return {"status": "success", "written_rows": len(summaries)}
