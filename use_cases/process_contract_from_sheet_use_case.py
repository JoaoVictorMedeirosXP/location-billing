from services.rental_contract_service import RentalContractService
from services.contract_monitoring_service import ContractMonitoringService
from services.write_summay_service import SheetsWriterService
from services.summary_service import SummaryService


class ProcessContractsFromSheetUseCase:
    def __init__(
        self,
        rental_service: RentalContractService,
        monitoring_service: ContractMonitoringService,
        writer_service: SheetsWriterService,
        summary_service: SummaryService,
    ):
        self.rental_service = rental_service
        self.monitoring_service = monitoring_service
        self.writer_service = writer_service
        self.summary_service = summary_service

    def execute(self, target_date: str) -> int:
        print("Use case, process contracts from sheets")
        cnpjs = self.monitoring_service.get_cnpjs("E")

        rental_contracts = self.rental_service.process_rental_contracts(
            cnpj_list=cnpjs, target_date=target_date
        )

        summaries = [
            self.summary_service(contract).process_summary()
            for contract in rental_contracts
        ]

        self.writer_service.append_table_with_header(data=summaries)

        return len(summaries)
