from google.cloud import firestore
from google.oauth2 import service_account
from config.settings import SERVICE_ACCOUNT_FILE


class FirestoreRepository:
    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE
        )
        self.client = firestore.Client(credentials=credentials)

    def get_contracts_by_cnpjs(self, cnpjs: list):
        contracts_data = []
        chunk_size = 10

        for i in range(0, len(cnpjs), chunk_size):
            chunk = cnpjs[i:i + chunk_size]
            query = (
                self.client.collection("rentalContracts")
                .where("cnpj", "in", chunk)
            )

            docs = query.stream()
            for doc in docs:
                contracts_data.append(doc.to_dict())

        return contracts_data
