from services.rental_contract_service import RentalContractService
from services.contract_monitoring_service import ContractMonitoringService
from repositories.bigquery_repository import BigQueryRepository
from repositories.firestore_repository import FirestoreRepository
from repositories.sheets_repository import GoogleSheetsRepository
from config.settings import SHEET_BILLS_NAME, SHEET_CONTRACTS_NAME


def main():

    rental_contract_service = RentalContractService(
        big_query_repo=BigQueryRepository(), firestore_repo=FirestoreRepository()
    )

    contract_monitoring_service = ContractMonitoringService(
        sheets_repo=GoogleSheetsRepository(SHEET_CONTRACTS_NAME)
    )

    cnpjs_list = contract_monitoring_service.get_cnpjs("E")
    print(rental_contract_service.process_active_contracts(cnpjs_list))

    return


if __name__ == "__main__":
    main()
