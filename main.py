from services.rental_contract_service import RentalContractService
from repositories.bigquery_repository import BigQueryRepository
from repositories.firestore_repository import FirestoreRepository

def main():
    
    rental_contract_service = RentalContractService(big_query_repo=BigQueryRepository,firestore_repo=FirestoreRepository)
    
    print(rental_contract_service.process_active_contracts())
   
  
    return

if __name__ == "__main__":
    main()