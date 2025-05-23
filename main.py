from config.settings import SHEET_BILLS_NAME, SHEET_CONTRACTS_NAME
from repositories.bigquery_repository import BigQueryRepository
from repositories.firestore_repository import FirestoreRepository
from repositories.sheets_repository import GoogleSheetsRepository
from services.contract_monitoring_service import ContractMonitoringService
from services.rental_contract_service import RentalContractService
from services.summary_service import SummaryService
from services.write_summay_service import SheetsWriterService


def main():

    rental_contract_service = RentalContractService(
        big_query_repo=BigQueryRepository(), firestore_repo=FirestoreRepository()
    )

    contract_monitoring_service = ContractMonitoringService(
        sheets_repo=GoogleSheetsRepository(SHEET_CONTRACTS_NAME)
    )

    cnpjs_list = contract_monitoring_service.get_cnpjs("E")

    rental_contracts = rental_contract_service.process_rental_contracts(cnpjs_list, target_date="2025-04-01")

    summaries = [
        SummaryService(rental_contract).process_summary()
        for rental_contract in rental_contracts
    ]

    sheets_writer_service = SheetsWriterService(
        sheets_repo=GoogleSheetsRepository(work_sheet=SHEET_BILLS_NAME)
    )
    
    sheets_writer_service.append_table_with_header(data=summaries)

    return


if __name__ == "__main__":
    main()
