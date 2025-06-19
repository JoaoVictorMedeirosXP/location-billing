from services.rental_contract_service import RentalContractService
from services.contract_monitoring_service import ContractMonitoringService
from services.summary_service import SummaryService
from services.write_summay_service import SheetsWriterService

from repositories.bigquery_repository import BigQueryRepository
from repositories.firestore_repository import FirestoreRepository
from repositories.sheets_repository import GoogleSheetsRepository

from config.settings import SHEET_BILLS_NAME, SHEET_CONTRACTS_NAME
from use_cases.process_contract_from_sheet_use_case import (
    ProcessContractsFromSheetUseCase,
)


def make_legacy_process_contracts_use_case() -> ProcessContractsFromSheetUseCase:
    rental_service = RentalContractService(
        big_query_repo=BigQueryRepository(), firestore_repo=FirestoreRepository()
    )

    monitoring_service = ContractMonitoringService(
        sheets_repo=GoogleSheetsRepository(SHEET_CONTRACTS_NAME)
    )

    writer_service = SheetsWriterService(
        sheets_repo=GoogleSheetsRepository(SHEET_BILLS_NAME)
    )

    return ProcessContractsFromSheetUseCase(
        rental_service=rental_service,
        monitoring_service=monitoring_service,
        writer_service=writer_service,
        summary_service=SummaryService,
    )


def make_process_contracts_use_case() -> ProcessContractsFromSheetUseCase:

    return
