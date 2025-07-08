from config.settings import (
    SHEET_BILLS_NAME,
    SHEET_CONTRACTS_NAME,
    SHEET_CONTRACTS_NEW_NAME,
    SHEET_UNITS_NAME,
)
from src.adapters.bigquery.bigquery_bills_repository import BigQueryBillsRepository
from src.adapters.firestore.firestore_bills_repository import FirestoreBillsRepository
from src.adapters.firestore.firestore_contracts_repository import (
    FirestoreContractsRepository,
)
from src.adapters.sheets.sheets_contract_summary_repository import (
    SheetsContractSummaryRepository,
)
from src.adapters.sheets.sheets_contracts_repository import SheetsContractsRepository
from src.adapters.sheets.sheets_units_repository import SheetsUnitsRepository
from src.services.check_unit_is_gd_service import CheckUnitIsGdService
from src.services.contract_monitoring_service import ContractMonitoringService
from src.services.rental_contracts_summary_service import RentalSummaryContractsService
from src.services.rental_relational_contract_service import (
    RentalRelationalContractService,
)
from src.services.summary_service import SummaryService
from src.services.write_summary_service import SheetsWriterService
from src.use_cases.process_contract_from_sheet_use_case import (
    ProcessContractsFromSheetUseCase,
)
from src.use_cases.summary_by_message_use_case import SummaryByMessageUseCase


def make_legacy_process_contracts_use_case() -> ProcessContractsFromSheetUseCase:
    rental_service = RentalSummaryContractsService(
        contracts_repo=FirestoreContractsRepository(),
        bills_repo=BigQueryBillsRepository(),
    )

    monitoring_service = ContractMonitoringService(
        contracts_repo=SheetsContractsRepository(SHEET_CONTRACTS_NAME)
    )

    writer_service = SheetsWriterService(
        contract_summary_repo=SheetsContractSummaryRepository(SHEET_BILLS_NAME)
    )

    return ProcessContractsFromSheetUseCase(
        rental_summary_service=rental_service,
        monitoring_service=monitoring_service,
        writer_service=writer_service,
        summary_service=SummaryService,
    )


def make_summary_by_message_use_case() -> SummaryByMessageUseCase:

    check_unit_is_gd_service = CheckUnitIsGdService(
        units_repo=SheetsUnitsRepository(work_sheet=SHEET_UNITS_NAME)
    )

    rental_summary_service = RentalRelationalContractService(
        contract_repo=SheetsContractsRepository(work_sheet=SHEET_CONTRACTS_NEW_NAME),
        bills_repo=FirestoreBillsRepository(),
        units_repo=SheetsUnitsRepository(work_sheet=SHEET_UNITS_NAME),
    )

    writer_service = SheetsWriterService(
        contract_summary_repo=SheetsContractSummaryRepository(SHEET_BILLS_NAME)
    )

    return SummaryByMessageUseCase(
        check_unit_is_gd_service=check_unit_is_gd_service,
        rental_relational_contract_service=rental_summary_service,
        summary_service=SummaryService,
        writer_summary_service=writer_service
    )
