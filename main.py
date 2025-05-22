from config.settings import SHEET_BILLS_NAME, SHEET_CONTRACTS_NAME
from repositories.bigquery_repository import BigQueryRepository
from repositories.firestore_repository import FirestoreRepository
from repositories.sheets_repository import GoogleSheetsRepository
from services.contract_monitoring_service import ContractMonitoringService
from services.rental_contract_service import RentalContractService
from services.summary_service import Summary


def main():

    rental_contract_service = RentalContractService(
        big_query_repo=BigQueryRepository(), firestore_repo=FirestoreRepository()
    )

    contract_monitoring_service = ContractMonitoringService(
        sheets_repo=GoogleSheetsRepository(SHEET_CONTRACTS_NAME)
    )

    cnpjs_list = contract_monitoring_service.get_cnpjs("E")

    rental_contracts = rental_contract_service.process_rental_contracts(cnpjs_list)

    summaries = [Summary(rental_contract).process_summary() for rental_contract in rental_contracts]
    
    print(summaries)

    return


if __name__ == "__main__":
    main()
