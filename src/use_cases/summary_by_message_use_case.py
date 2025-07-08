from src.services.check_unit_is_gd_service import CheckUnitIsGdService
from src.services.rental_relational_contract_service import (
    RentalRelationalContractService,
)
from src.services.summary_service import SummaryService
from src.services.write_summary_service import SheetsWriterService


class SummaryByMessageUseCase:

    def __init__(
        self,
        check_unit_is_gd_service: CheckUnitIsGdService,
        rental_relational_contract_service: RentalRelationalContractService,
        writer_summary_service: SheetsWriterService,
        summary_service: SummaryService,
    ):

        self.check_unit_is_gd_service = check_unit_is_gd_service
        self.rental_relational_contract_service = rental_relational_contract_service
        self.summary_service = summary_service
        self.writer_summary_service = writer_summary_service

    def execute(self, message):

        check = self.check_unit_is_gd_service.execute(message)

        if not check:
            return {"status": "pass"}

        rental_contracts = self.rental_relational_contract_service.execute()

        summaries = [
            self.summary_service(contract).process_summary()
            for contract in rental_contracts
        ]

        self.writer_summary_service.overwrite_table_with_header(data=summaries)

        return {"status": "success", "written_rows": len(summaries)}
