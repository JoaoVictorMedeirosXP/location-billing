from services.rental_contracts_summary_service import RentalSummaryContractsService
from services.contract_monitoring_service import ContractMonitoringService
from services.write_summary_service import SheetsWriterService
from services.summary_service import SummaryService

from utils.reference_month import ReferenceMonth


class SummaryByMessageUseCase:

    def __init__(
        self,
        check_unit_is_gd_service,
        rental_summary_service: RentalSummaryContractsService,
        monitoring_service: ContractMonitoringService,
        summary_service: SummaryService,
        writer_service: SheetsWriterService,
    ):

        self.check_unit_is_gd_service = check_unit_is_gd_service
        self.rental_summary_service = rental_summary_service
        self.summary_service = summary_service
        self.monitoring_service = monitoring_service
        self.writer_service = writer_service
        return

    def execute(self, account_contract):

        check = self.check_unit_is_gd_service.check_unit(account_contract)

        if not check:
            return {"status": "pass"}

        cnpjs = self.monitoring_service.get_cnpjs("E")

        rental_contracts = self.rental_summary_service.execute(
            cnpj_list=cnpjs, target_date=ReferenceMonth.current().as_string
        )

        summaries = [
            self.summary_service(contract).process_summary()
            for contract in rental_contracts
        ]

        self.writer_service.append_table_with_header(data=summaries)

        return {"status": "success", "written_rows": len(summaries)}
