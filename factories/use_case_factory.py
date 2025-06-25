from services.rental_contracts_summary_service import RentalSummaryContractsService
from services.contract_monitoring_service import ContractMonitoringService
from services.summary_service import SummaryService
from services.write_summary_service import SheetsWriterService

from infrastructure.bigquery.bigquery_repository import BigQueryBillsRepository
from infrastructure.firestore.firestore_contracts_repository import (
    FirestoreContractsRepository,
)
from repositories.sheets_repository import GoogleSheetsRepository

from config.settings import SHEET_BILLS_NAME, SHEET_CONTRACTS_NAME
from use_cases.process_contract_from_sheet_use_case import (
    ProcessContractsFromSheetUseCase,
)


def make_legacy_process_contracts_use_case() -> ProcessContractsFromSheetUseCase:
    rental_service = RentalSummaryContractsService(
        contracts_repo=FirestoreContractsRepository(), bills_repo=BigQueryBillsRepository()
    )

    monitoring_service = ContractMonitoringService(
        sheets_repo=GoogleSheetsRepository(SHEET_CONTRACTS_NAME)
    )

    writer_service = SheetsWriterService(
        sheets_repo=GoogleSheetsRepository(SHEET_BILLS_NAME)
    )

    return ProcessContractsFromSheetUseCase(
        rental_summary_service=rental_service,
        monitoring_service=monitoring_service,
        writer_service=writer_service,
        summary_service=SummaryService,
    )


def make_process_contracts_use_case() -> ProcessContractsFromSheetUseCase:

    return
